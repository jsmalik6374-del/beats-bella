import http.server
import socketserver
import urllib.parse
import os

PORT = int(os.environ.get('PORT', 5000))

WHATSAPP_NUMBER = "=923234207513"

class BeatsBellaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/order'):
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            item = query_params.get('item', [''])[0]
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html_form = f"""
            <!doctype html>
            <html>
              <head>
                <title>Beats Bella - Order Form</title>
                <style>
                  body {{ font-family: Arial, sans-serif; background: #f9f9f9; padding: 30px; text-align: center; }}
                  .form-box {{ background: white; padding: 25px; margin: auto; width: 320px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                  input, textarea, select {{ padding: 10px; width: 280px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }}
                  button {{ padding: 12px 20px; background: #25D366; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; }}
                </style>
              </head>
              <body>
                <div class="form-box">
                  <h2>Beats Bella Order</h2>
                  <p>Item: <b>{item}</b></p>
                  <form action="/submit" method="POST">
                    <input type="hidden" name="item" value="{item}">
                    <input type="text" name="name" placeholder="Aapka Naam" required><br>
                    <input type="text" name="phone" placeholder="Phone Number (03XX-XXXXXXX)" required><br>
                    <select name="area" required>
                      <option value="">Select Lahore Area</option>
                      <option value="Gulberg">Gulberg</option>
                      <option value="DHA">DHA</option>
                      <option value="Johar Town">Johar Town</option>
                      <option value="Model Town">Model Town</option>
                      <option value="Bahria Town">Bahria Town</option>
                      <option value="Other Lahore Area">Other Lahore Area</option>
                    </select><br>
                    <textarea name="address" placeholder="Complete Delivery Address in Lahore" required></textarea><br>
                    <button type="submit">Send Order on WhatsApp</button>
                  </form>
                  <br><a href="/" style="text-decoration: none; color: #007bff;">Back to Home</a>
                </div>
              </body>
            </html>
            """
            self.wfile.write(html_form.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            
            name = parsed_data.get('name', [''])[0]
            phone = parsed_data.get('phone', [''])[0]
            area = parsed_data.get('area', [''])[0]
            address = parsed_data.get('address', [''])[0]
            item = parsed_data.get('item', [''])[0]
            
            msg = f"Hello Beats Bella! Mera naam {name} hai. Mujhe yeh order karna hai (Home Delivery in Lahore):\n\n*Product:* {item}\n*Phone:* {phone}\n*Area:* {area}\n*Address:* {address}"
            encoded_msg = urllib.parse.quote(msg)
            whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"
            
            self.send_response(303)
            self.send_header('Location', whatsapp_url)
            self.end_headers()

# HTML Home Page with Products and Pictures
index_html = """
<!doctype html>
<html>
  <head>
    <title>Beats Bella Official Store</title>
    <style>
      body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; text-align: center; margin: 0; }
      .header { background: #ff4757; color: white; padding: 25px; border-radius: 0 0 15px 15px; margin-bottom: 30px; }
      .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; max-width: 1000px; margin: auto; }
      .card { background: white; padding: 15px; width: 260px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
      .card img { width: 100%; height: 180px; object-fit: cover; border-radius: 8px; }
      .btn { background: #25D366; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 10px; font-weight: bold;}
      .btn:hover { background: #1ebe5d; }
      .tag { color: #555; font-size: 14px; margin: 5px 0; }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>Beats Bella 🎶🛍️</h1>
      <p>Exclusive Handcrafted Accessories | Home Delivery Available Across Lahore</p>
    </div>
    
    <div class="container">
      <!-- Product 1 -->
      <div class="card">
        <img src="ring.jpg" alt="Beats Bella Special Ring">
        <h3>Special Ring</h3>
        <p class="tag">Aapi ka exclusive handmade ring</p>
        <p><b>Rs. 1,200</b></p>
        <a href="/order?item=Beats+Bella+Special+Ring" class="btn">Order on WhatsApp</a>
      </div>

      <!-- Product 2 -->
      <div class="card">
        <img src="bracelet.jpg" alt="Beats Bella Bracelet">
        <h3>Trendy Bracelet</h3>
        <p class="tag">Stylish and aesthetic design</p>
        <p><b>Rs. 1,500</b></p>
        <a href="/order?item=Beats+Bella+Trendy+Bracelet" class="btn">Order on WhatsApp</a>
      </div>
    </div>
  </body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

with socketserver.TCPServer(("", PORT), BeatsBellaHandler) as httpd:
    print(f"Beats Bella Server started on port {PORT}...")
    httpd.serve_forever()
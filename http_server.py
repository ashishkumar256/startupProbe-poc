import http.server
import socketserver
import threading
import time
import redis

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/init':
            # Simulate initialization process including Redis connectivity
            redis_connection = None
            try:
                # Simulate establishing connection to Redis
                redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
                redis_connection.ping()  # Check if Redis is reachable
                #time.sleep(5)  # Simulate other initialization tasks
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Initialization completed\n')
            except Exception as e:
                # Handle initialization failure
                if redis_connection:
                    redis_connection.close()
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Initialization failed: {str(e)}'.encode('utf-8'))
        elif self.path == '/health':
            # Health check
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Application is up & running\n')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found\n')

def start_server():
    PORT = 8080
    Handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server started at localhost:{}".format(PORT))
        httpd.serve_forever()

# Start the HTTP server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Allow the main thread to exit even if this thread is running
server_thread.start()

# Keep the main thread alive
while True:
    time.sleep(1)


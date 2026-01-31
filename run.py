from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application
    # debug=True enables auto-reload and detailed error pages
    # Set debug=False for production
    print("Starting Face Detection Web Application...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")

    app.run(
        debug=True,
        host='0.0.0.0',  # Makes server accessible from other devices on network
        port=5000
    )

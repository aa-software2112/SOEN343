import pytest

from app import app

# When put under app.run, wouldn't run until server would be shut off
#pytest.main()

# Runs the app with a direct call "python __init__.py"
if __name__ == "__main__":
    app.run(debug=True)


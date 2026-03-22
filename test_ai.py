from ai_healer import get_new_locator

html_string = """
<html>
<body>
    <form>
        <input type="text" id="username">
        <input type="password" id="password">
        <button id="submit-action-btn">Login</button>
    </form>
</body>
</html>
"""

old_locator = "login-btn"

new_locator = get_new_locator(html_string, old_locator)

print("Recovered Locator:", new_locator)
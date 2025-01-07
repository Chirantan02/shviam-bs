import markdown

try:
    import markdown
    print("Markdown library is available.")
except ImportError:
    print("Markdown library is NOT available.")

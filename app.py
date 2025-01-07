from flask import Flask, render_template, request
import ollama
import markdown2  # Import the markdown2 library

app = Flask(__name__)

# Home route to display the form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle article generation
@app.route('/generate', methods=['POST'])
def generate():
    # Extract form data
    target_keyword = request.form.get('target_keyword')
    article_length = request.form.get('article_length')
    tone_of_voice = request.form.get('tone_of_voice')
    language = request.form.get('language')

    # Create a prompt based on user inputs
    prompt = f"Write a {article_length} article in {tone_of_voice} tone about {target_keyword} in {language}."

    # Generate the article using the API
    generated_article = ""
    try:
        messages = [{'role': 'user', 'content': prompt}]
        stream = ollama.chat(model='llama3.1', messages=messages, stream=False)  # Use non-streaming for full response
        generated_article = stream['message']['content']
        
        # Convert Markdown to HTML using markdown2
        generated_article = markdown2.markdown(generated_article)
    except ollama.ResponseError as e:
        generated_article = f"Error: {e.content}"
    except Exception as e:
        generated_article = f"An unexpected error occurred: {str(e)}"

    # Render the result template with the generated article
    return render_template('result.html', article=generated_article)

if __name__ == '__main__':
    app.run(debug=True)

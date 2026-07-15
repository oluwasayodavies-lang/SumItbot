import os
import openai
from config import Config

# Initialize OpenAI
openai.api_key = Config.OPENAI_API_KEY

async def summarize_text(text: str, length: str = "medium") -> str:
    """
    Summarize text using OpenAI API.
    
    Args:
        text: Text to summarize
        length: 'short', 'medium', or 'long'
    
    Returns:
        Summarized text
    """
    word_count = Config.SUMMARY_LENGTHS.get(length, 100)
    
    prompt = f"""
    Please summarize the following text in approximately {word_count} words.
    Make the summary clear, concise, and capture the main points.
    
    Text: {text}
    
    Summary:
    """
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=word_count * 2,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

async def summarize_document(file_path: str, length: str = "medium") -> str:
    """
    Summarize document content.
    
    Args:
        file_path: Path to document file
        length: 'short', 'medium', or 'long'
    
    Returns:
        Summarized text
    """
    # Extract text from document
    text = await extract_text_from_document(file_path)
    
    # Summarize the extracted text
    return await summarize_text(text, length)

async def extract_text_from_document(file_path: str) -> str:
    """
    Extract text from various document formats.
    
    Supports: .txt, .pdf, .docx, .md, .rtf
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.txt' or file_extension == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_extension == '.pdf':
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        
        elif file_extension == '.docx':
            import docx
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        
        elif file_extension == '.rtf':
            from striprtf.striprtf import rtf_to_text
            with open(file_path, 'r', encoding='utf-8') as f:
                return rtf_to_text(f.read())
        
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
    except Exception as e:
        raise Exception(f"Failed to extract text: {str(e)}")

def set_summary_length(context, length: str) -> bool:
    """Set user's preferred summary length."""
    if length not in Config.SUMMARY_LENGTHS:
        return False
    
    context.user_data['summary_length'] = length
    return True

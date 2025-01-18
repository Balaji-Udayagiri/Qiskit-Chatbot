import unicodedata

def clean_output(output):
    """
    Remove unwanted lines from the output, such as warnings or extra messages.
    """
    lines = output.splitlines()
    filtered_lines = [line for line in lines if not line.startswith("failed to get console mode")]
    return "\n".join(filtered_lines)

def extract_imports(prompt):
    """
    Extract import statements from the prompt.
    """
    imports = []
    for line in prompt.splitlines():
        line = line.strip()
        if line.startswith("import") or line.startswith("from"):
            imports.append(line)
    return "\n".join(imports)

def check_for_imports(code):
    """
    Check if the prompt contains import statements.
    """
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("import") or line.startswith("from"):
            return True
    return False

def check_for_defs(code):
    """
    Check if the prompt contains function definitions.
    """
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def"):
            return True
    return False

def extract_def(prompt):
    """
    Extract function definitions from the prompt.
    """
    defs = []
    for line in prompt.splitlines():
        line = line.strip()
        if line.startswith("def"):
            defs.append(line)
    #print("defs: ", defs)
    return "\n".join(defs)

def combine_imports(prompt, code):
    """
    Combine imports from the prompt with the code.
    """
    checkForDef = check_for_defs(code)
    checkForImport = check_for_imports(code)

    if checkForDef and checkForImport:
        return code
    # if prompt_imports in code and def_imports in code:
    #     return code  # Use the entire generated code if it already contains imports and function definitions

    
    else:
        indented_code = ""
        for i, line in enumerate(code.splitlines()):
            if i == 0:
                indented_code = f"    {line}\n"
            else:
                indented_code += f"{line}\n"

        code = prompt + "\n" + indented_code
        return code

def normalize_code(code_str):
    """
    Normalize the code to remove problematic characters and ensure compatibility.
    - Convert special Unicode characters to ASCII equivalents where possible.
    - Remove or replace characters that cannot be encoded in UTF-8.
    """
    normalized_code = unicodedata.normalize('NFKD', code_str).encode('ascii', 'ignore').decode('ascii')
    return normalized_code

def extract_code(gpt_response):
    """
    Extract the Python code from GPT response by looking for triple backticks.
    """
    if "```" in gpt_response:
        code_blocks = gpt_response.split("```")
        for block in code_blocks:
            if block.strip().startswith("python") or block.strip().startswith("from") or block.strip().startswith("def"):
                return block.strip().lstrip("python").strip()
    return gpt_response  # Fallback: return the full response if no delimiters are found

def process_LLM_output(code, prompt):
    extracted_code = extract_code(code)
    print(f"Extracted Code:\n{extracted_code}\n")

    # Combine imports from the prompt and normalize code

    complete_code = combine_imports(prompt, extracted_code)
    complete_code = normalize_code(complete_code)


    print(f"Complete Code with Imports and Normalized:\n{complete_code}\n")
    return complete_code

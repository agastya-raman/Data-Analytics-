import os
from dotenv import load_dotenv
load_dotenv()

def run_code(code: str, dataset_path: str) -> dict:
    try:
        from e2b_code_interpreter import Sandbox
        with Sandbox() as sbx:
            with open(dataset_path, "rb") as f:
                sbx.files.write("/home/user/dataset.csv", f)
            execution = sbx.run_code(code)
            return {
                "success": not execution.error,
                "stdout":  "\n".join(execution.logs.stdout),
                "stderr":  "\n".join(execution.logs.stderr),
                "error":   str(execution.error) if execution.error else None,
                "result":  execution.results[0].text if execution.results else None
            }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": "", "error": str(e), "result": None}
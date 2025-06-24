import os
import secrets
import requests
from bs4 import BeautifulSoup
import argparse
class ArgumentParsing:
    def __init__(self):
        args = argparse.ArgumentParser("jsFuzzer",usage="jsFuzzer.py target",description="fast JavaScript Fuzz Tool")
        args.add_argument("target",help="your target (example:https://www.example.com)")
        self.parser = args.parse_args()
class Fuzzer :
    def __init__(self,url):
        self.__url = url
    def fetch_content(self):
        self.request = requests.get(self.__url,headers={
            "User-Agent":"Mozilla Firefox"
        })
        self.text = self.request.text
        return self.text
    def extractJs(self,pas):
        self.soup = BeautifulSoup(self.fetch_content(),"html.parser")
        for i in self.soup.find_all("script"):
            src = i.get("src")
            if src:
                print("[>>] External JavaScript File Found : " + src)
            if i.string:
                output_dir = os.path.join(os.getcwd(), "javascript_output")
                os.makedirs(output_dir, exist_ok=True)
                filename =f"{pas}___{secrets.token_hex(8)}.js"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(i.string)
                print(f"[>>] Inline JavaScript saved to: {filepath}")

arg = ArgumentParsing()
remove_protocal = arg.parser.target[len("https://www."):]
fuzz = Fuzzer(arg.parser.target)
fuzz.extractJs(remove_protocal)
import base64
from openai import OpenAI


class ImgDetection:
    def __init__(self):
        # self.llm = OpenAI(temperature=0.7)
        self.client = OpenAI()
        self.model_name = "gpt-4o"
        self.sys_prompt = """You are an image analysis assistant. You are given an image in base64 and your task is to 
        detect bottles present in the image, count them, and return the result as a dictionary. 
        The dictionary should contain the following 
        format:\n\n{\n  'bottle_name_1': count_1,\n  'bottle_name_2': count_2,\n  ...\n}\n\n
        If you cannot identify the bottle type, label it as 'unknown_bottle'. Ensure that the count represents the exact 
        number of each bottle type identified in the image. The response should be accurate, concise, and should only include 
        the bottles detected. """
        self.prompt2 = """
        analyze image and provide data in table format as bottle name and its count. 
        analyze all bottles and respectively increase their count.
        if bottles are not readable. zoom in image and detect bottle names from their text.
        at end add total bottles counted.
        """

    def to_base64(self, filedata):
        try:
            # image = open(filename, "rb",).read()
            return base64.b64encode(filedata).decode("utf-8")
        except Exception as base64_err:
            print("Couldn't read the image. Make sure the path is correct and the file exists.")
            raise base64_err
            # exit()

    def create_prompt(self, image_url: str):
        return self.sys_prompt + image_url
    
    def detect(self, image_file: str):
        b64img = self.to_base64(image_file)
        resopnse = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt2,
                },
                {
                    "role": "user",
                    "content": [
                        # {"type": "text", "text": "Bottle names and their count from image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64img}"},
                        },
                    ],
                },
            ],
            max_tokens=1000,
            # stream=True,
        )
        return resopnse.choices[0].message.content

    def detect_obj(self, image_url: str):
        # response = self.llm.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system", "content": "You are an image analysis assistant. detect beer and wine bottles in images and get name of bottle from name on bottle. Return dictionry of bottle name and its count. you will be provided image url only"},
        #         {"role": "user", "content": image_url}
        #     ],
        # )
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": """You are an image analysis assistant. 
                    You are given an image or image in base64
                    Your task is to detect bottles present in the image, count them, and return the result as a dictionary. 
                    The dictionary contain image names and its count
                    Ensure that the count represents the exact number of each bottle type identified in the image. The response should be accurate, concise, and should only include the bottles detected.
                    add undetected bottles as unknown_bottle name"""},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                    },
                ],
                }
            ],
        )

        return response.choices[0].message


if __name__ == '__main__':
    file = "/Users/vishvaraj/projects/img-obj-detection-service/6e3bcaa3-IMG_7479.jpeg"
    data = open(file, 'rb').read()
    img = ImgDetection()
    res = img.detect(image_file=data)
    print(res)

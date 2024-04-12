from dotenv import load_dotenv
import fire


class BootStrap:
    pass


if __name__ == "__main__":
    load_dotenv()
    fire.Fire(BootStrap)
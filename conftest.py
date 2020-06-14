def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://reqres.in/",
        help="reqres url"
    )

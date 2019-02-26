from сlient.Client import Client


if __name__ == "__main__":
    client = Client()
    while client.request():
        pass
    client.close()

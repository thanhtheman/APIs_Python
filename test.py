a = [{"message": 'len', "id": 6}, {"message": 'daniel', "id": 5}, {"message": 'lento', "id": 8}]


def find_index(id):
    for i, p in enumerate(a):
        if p["id"] == id:
            print(i)

find_index(5)

defmodule MangaService.CollectionDBTest do
  use MangaService.DataCase

  alias MangaService.CollectionDB

  describe "collection" do
    alias MangaService.CollectionDB.Collection

    import MangaService.CollectionDBFixtures

    @invalid_attrs %{id: nil, read: nil, store: nil, collection: nil, user_id: nil, isbn: nil, cost: nil, purchase_date: nil, tags: nil, rating: nil}

    test "list_collection/0 returns all collection" do
      collection = collection_fixture()
      assert CollectionDB.list_collection() == [collection]
    end

    test "get_collection!/1 returns the collection with given id" do
      collection = collection_fixture()
      assert CollectionDB.get_collection!(collection.id) == collection
    end

    test "create_collection/1 with valid data creates a collection" do
      valid_attrs = %{id: "some id", read: true, store: "some store", collection: "some collection", user_id: "some user_id", isbn: "some isbn", cost: 120.5, purchase_date: ~D[2024-11-02], tags: ["option1", "option2"], rating: 120.5}

      assert {:ok, %Collection{} = collection} = CollectionDB.create_collection(valid_attrs)
      assert collection.id == "some id"
      assert collection.read == true
      assert collection.store == "some store"
      assert collection.collection == "some collection"
      assert collection.user_id == "some user_id"
      assert collection.isbn == "some isbn"
      assert collection.cost == 120.5
      assert collection.purchase_date == ~D[2024-11-02]
      assert collection.tags == ["option1", "option2"]
      assert collection.rating == 120.5
    end

    test "create_collection/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = CollectionDB.create_collection(@invalid_attrs)
    end

    test "update_collection/2 with valid data updates the collection" do
      collection = collection_fixture()
      update_attrs = %{id: "some updated id", read: false, store: "some updated store", collection: "some updated collection", user_id: "some updated user_id", isbn: "some updated isbn", cost: 456.7, purchase_date: ~D[2024-11-03], tags: ["option1"], rating: 456.7}

      assert {:ok, %Collection{} = collection} = CollectionDB.update_collection(collection, update_attrs)
      assert collection.id == "some updated id"
      assert collection.read == false
      assert collection.store == "some updated store"
      assert collection.collection == "some updated collection"
      assert collection.user_id == "some updated user_id"
      assert collection.isbn == "some updated isbn"
      assert collection.cost == 456.7
      assert collection.purchase_date == ~D[2024-11-03]
      assert collection.tags == ["option1"]
      assert collection.rating == 456.7
    end

    test "update_collection/2 with invalid data returns error changeset" do
      collection = collection_fixture()
      assert {:error, %Ecto.Changeset{}} = CollectionDB.update_collection(collection, @invalid_attrs)
      assert collection == CollectionDB.get_collection!(collection.id)
    end

    test "delete_collection/1 deletes the collection" do
      collection = collection_fixture()
      assert {:ok, %Collection{}} = CollectionDB.delete_collection(collection)
      assert_raise Ecto.NoResultsError, fn -> CollectionDB.get_collection!(collection.id) end
    end

    test "change_collection/1 returns a collection changeset" do
      collection = collection_fixture()
      assert %Ecto.Changeset{} = CollectionDB.change_collection(collection)
    end
  end
end

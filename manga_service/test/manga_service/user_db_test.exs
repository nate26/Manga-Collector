defmodule MangaService.UserDBTest do
  use MangaService.DataCase

  alias MangaService.UserDB

  describe "users" do
    alias MangaService.UserDB.User

    import MangaService.UserDBFixtures

    @invalid_attrs %{id: nil, color: nil, username: nil, password: nil, email: nil, collection_id: nil, picture: nil, banner: nil, theme: nil, personal_stores: nil}

    test "list_users/0 returns all users" do
      user = user_fixture()
      assert UserDB.list_users() == [user]
    end

    test "get_user!/1 returns the user with given id" do
      user = user_fixture()
      assert UserDB.get_user!(user.id) == user
    end

    test "create_user/1 with valid data creates a user" do
      valid_attrs = %{id: "some id", color: "some color", username: "some username", password: "some password", email: "some email", collection_id: "some collection_id", picture: "some picture", banner: "some banner", theme: "some theme", personal_stores: ["option1", "option2"]}

      assert {:ok, %User{} = user} = UserDB.create_user(valid_attrs)
      assert user.id == "some id"
      assert user.color == "some color"
      assert user.username == "some username"
      assert user.password == "some password"
      assert user.email == "some email"
      assert user.collection_id == "some collection_id"
      assert user.picture == "some picture"
      assert user.banner == "some banner"
      assert user.theme == "some theme"
      assert user.personal_stores == ["option1", "option2"]
    end

    test "create_user/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = UserDB.create_user(@invalid_attrs)
    end

    test "update_user/2 with valid data updates the user" do
      user = user_fixture()
      update_attrs = %{id: "some updated id", color: "some updated color", username: "some updated username", password: "some updated password", email: "some updated email", collection_id: "some updated collection_id", picture: "some updated picture", banner: "some updated banner", theme: "some updated theme", personal_stores: ["option1"]}

      assert {:ok, %User{} = user} = UserDB.update_user(user, update_attrs)
      assert user.id == "some updated id"
      assert user.color == "some updated color"
      assert user.username == "some updated username"
      assert user.password == "some updated password"
      assert user.email == "some updated email"
      assert user.collection_id == "some updated collection_id"
      assert user.picture == "some updated picture"
      assert user.banner == "some updated banner"
      assert user.theme == "some updated theme"
      assert user.personal_stores == ["option1"]
    end

    test "update_user/2 with invalid data returns error changeset" do
      user = user_fixture()
      assert {:error, %Ecto.Changeset{}} = UserDB.update_user(user, @invalid_attrs)
      assert user == UserDB.get_user!(user.id)
    end

    test "delete_user/1 deletes the user" do
      user = user_fixture()
      assert {:ok, %User{}} = UserDB.delete_user(user)
      assert_raise Ecto.NoResultsError, fn -> UserDB.get_user!(user.id) end
    end

    test "change_user/1 returns a user changeset" do
      user = user_fixture()
      assert %Ecto.Changeset{} = UserDB.change_user(user)
    end
  end
end

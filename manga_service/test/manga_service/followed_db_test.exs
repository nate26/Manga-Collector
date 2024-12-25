defmodule MangaService.FollowedDBTest do
  use MangaService.DataCase

  alias MangaService.FollowedDB

  describe "followed" do
    alias MangaService.FollowedDB.Followed

    import MangaService.FollowedDBFixtures

    @invalid_attrs %{user_id: nil, follow_type: nil, follow_id: nil}

    test "list_followed/0 returns all followed" do
      followed = followed_fixture()
      assert FollowedDB.list_followed() == [followed]
    end

    test "get_followed!/1 returns the followed with given id" do
      followed = followed_fixture()
      assert FollowedDB.get_followed!(followed.id) == followed
    end

    test "create_followed/1 with valid data creates a followed" do
      valid_attrs = %{user_id: "some user_id", follow_type: "some follow_type", follow_id: "some follow_id"}

      assert {:ok, %Followed{} = followed} = FollowedDB.create_followed(valid_attrs)
      assert followed.user_id == "some user_id"
      assert followed.follow_type == "some follow_type"
      assert followed.follow_id == "some follow_id"
    end

    test "create_followed/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = FollowedDB.create_followed(@invalid_attrs)
    end

    test "update_followed/2 with valid data updates the followed" do
      followed = followed_fixture()
      update_attrs = %{user_id: "some updated user_id", follow_type: "some updated follow_type", follow_id: "some updated follow_id"}

      assert {:ok, %Followed{} = followed} = FollowedDB.update_followed(followed, update_attrs)
      assert followed.user_id == "some updated user_id"
      assert followed.follow_type == "some updated follow_type"
      assert followed.follow_id == "some updated follow_id"
    end

    test "update_followed/2 with invalid data returns error changeset" do
      followed = followed_fixture()
      assert {:error, %Ecto.Changeset{}} = FollowedDB.update_followed(followed, @invalid_attrs)
      assert followed == FollowedDB.get_followed!(followed.id)
    end

    test "delete_followed/1 deletes the followed" do
      followed = followed_fixture()
      assert {:ok, %Followed{}} = FollowedDB.delete_followed(followed)
      assert_raise Ecto.NoResultsError, fn -> FollowedDB.get_followed!(followed.id) end
    end

    test "change_followed/1 returns a followed changeset" do
      followed = followed_fixture()
      assert %Ecto.Changeset{} = FollowedDB.change_followed(followed)
    end
  end
end

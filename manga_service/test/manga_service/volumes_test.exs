defmodule MangaService.VolumesTest do
  use MangaService.DataCase

  alias MangaService.Volumes

  describe "volumes" do
    alias MangaService.Volumes.Volume

    import MangaService.VolumesFixtures

    @invalid_attrs %{name: nil, format: nil, description: nil, category: nil, url: nil, isbn: nil, brand: nil, series: nil, series_id: nil, edition: nil, edition_id: nil, display_name: nil, volume: nil, record_added_date: nil, record_updated_date: nil, release_date: nil, publisher: nil, pages: nil, authors: nil, isbn_10: nil, primary_cover_image: nil, cover_images: nil}

    test "list_volumes/0 returns all volumes" do
      volume = volume_fixture()
      assert Volumes.list_volumes() == [volume]
    end

    test "get_volume!/1 returns the volume with given id" do
      volume = volume_fixture()
      assert Volumes.get_volume!(volume.id) == volume
    end

    test "create_volume/1 with valid data creates a volume" do
      valid_attrs = %{name: "some name", format: "some format", description: "some description", category: "some category", url: "some url", isbn: "some isbn", brand: "some brand", series: "some series", series_id: "some series_id", edition: "some edition", edition_id: "some edition_id", display_name: "some display_name", volume: "some volume", record_added_date: ~N[2024-11-02 00:36:00], record_updated_date: ~N[2024-11-02 00:36:00], release_date: ~D[2024-11-02], publisher: "some publisher", pages: 42, authors: "some authors", isbn_10: "some isbn_10", primary_cover_image: "some primary_cover_image", cover_images: []}

      assert {:ok, %Volume{} = volume} = Volumes.create_volume(valid_attrs)
      assert volume.name == "some name"
      assert volume.format == "some format"
      assert volume.description == "some description"
      assert volume.category == "some category"
      assert volume.url == "some url"
      assert volume.isbn == "some isbn"
      assert volume.brand == "some brand"
      assert volume.series == "some series"
      assert volume.series_id == "some series_id"
      assert volume.edition == "some edition"
      assert volume.edition_id == "some edition_id"
      assert volume.display_name == "some display_name"
      assert volume.volume == "some volume"
      assert volume.record_added_date == ~N[2024-11-02 00:36:00]
      assert volume.record_updated_date == ~N[2024-11-02 00:36:00]
      assert volume.release_date == ~D[2024-11-02]
      assert volume.publisher == "some publisher"
      assert volume.pages == 42
      assert volume.authors == "some authors"
      assert volume.isbn_10 == "some isbn_10"
      assert volume.primary_cover_image == "some primary_cover_image"
      assert volume.cover_images == []
    end

    test "create_volume/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Volumes.create_volume(@invalid_attrs)
    end

    test "update_volume/2 with valid data updates the volume" do
      volume = volume_fixture()
      update_attrs = %{name: "some updated name", format: "some updated format", description: "some updated description", category: "some updated category", url: "some updated url", isbn: "some updated isbn", brand: "some updated brand", series: "some updated series", series_id: "some updated series_id", edition: "some updated edition", edition_id: "some updated edition_id", display_name: "some updated display_name", volume: "some updated volume", record_added_date: ~N[2024-11-03 00:36:00], record_updated_date: ~N[2024-11-03 00:36:00], release_date: ~D[2024-11-03], publisher: "some updated publisher", pages: 43, authors: "some updated authors", isbn_10: "some updated isbn_10", primary_cover_image: "some updated primary_cover_image", cover_images: []}

      assert {:ok, %Volume{} = volume} = Volumes.update_volume(volume, update_attrs)
      assert volume.name == "some updated name"
      assert volume.format == "some updated format"
      assert volume.description == "some updated description"
      assert volume.category == "some updated category"
      assert volume.url == "some updated url"
      assert volume.isbn == "some updated isbn"
      assert volume.brand == "some updated brand"
      assert volume.series == "some updated series"
      assert volume.series_id == "some updated series_id"
      assert volume.edition == "some updated edition"
      assert volume.edition_id == "some updated edition_id"
      assert volume.display_name == "some updated display_name"
      assert volume.volume == "some updated volume"
      assert volume.record_added_date == ~N[2024-11-03 00:36:00]
      assert volume.record_updated_date == ~N[2024-11-03 00:36:00]
      assert volume.release_date == ~D[2024-11-03]
      assert volume.publisher == "some updated publisher"
      assert volume.pages == 43
      assert volume.authors == "some updated authors"
      assert volume.isbn_10 == "some updated isbn_10"
      assert volume.primary_cover_image == "some updated primary_cover_image"
      assert volume.cover_images == []
    end

    test "update_volume/2 with invalid data returns error changeset" do
      volume = volume_fixture()
      assert {:error, %Ecto.Changeset{}} = Volumes.update_volume(volume, @invalid_attrs)
      assert volume == Volumes.get_volume!(volume.id)
    end

    test "delete_volume/1 deletes the volume" do
      volume = volume_fixture()
      assert {:ok, %Volume{}} = Volumes.delete_volume(volume)
      assert_raise Ecto.NoResultsError, fn -> Volumes.get_volume!(volume.id) end
    end

    test "change_volume/1 returns a volume changeset" do
      volume = volume_fixture()
      assert %Ecto.Changeset{} = Volumes.change_volume(volume)
    end
  end
end

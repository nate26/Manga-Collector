defmodule MangaService.BundlesTest do
  use MangaService.DataCase

  alias MangaService.Bundles

  describe "bundles" do
    alias MangaService.Bundles.Bundle

    import MangaService.BundlesFixtures

    @invalid_attrs %{item_id: nil, series_id: nil, shop_id: nil, volumes: nil, volume_start: nil, volume_end: nil}

    test "list_bundles/0 returns all bundles" do
      bundle = bundle_fixture()
      assert Bundles.list_bundles() == [bundle]
    end

    test "get_bundle!/1 returns the bundle with given id" do
      bundle = bundle_fixture()
      assert Bundles.get_bundle!(bundle.id) == bundle
    end

    test "create_bundle/1 with valid data creates a bundle" do
      valid_attrs = %{item_id: "some item_id", series_id: "some series_id", shop_id: "some shop_id", volumes: [], volume_start: "some volume_start", volume_end: "some volume_end"}

      assert {:ok, %Bundle{} = bundle} = Bundles.create_bundle(valid_attrs)
      assert bundle.item_id == "some item_id"
      assert bundle.series_id == "some series_id"
      assert bundle.shop_id == "some shop_id"
      assert bundle.volumes == []
      assert bundle.volume_start == "some volume_start"
      assert bundle.volume_end == "some volume_end"
    end

    test "create_bundle/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Bundles.create_bundle(@invalid_attrs)
    end

    test "update_bundle/2 with valid data updates the bundle" do
      bundle = bundle_fixture()
      update_attrs = %{item_id: "some updated item_id", series_id: "some updated series_id", shop_id: "some updated shop_id", volumes: [], volume_start: "some updated volume_start", volume_end: "some updated volume_end"}

      assert {:ok, %Bundle{} = bundle} = Bundles.update_bundle(bundle, update_attrs)
      assert bundle.item_id == "some updated item_id"
      assert bundle.series_id == "some updated series_id"
      assert bundle.shop_id == "some updated shop_id"
      assert bundle.volumes == []
      assert bundle.volume_start == "some updated volume_start"
      assert bundle.volume_end == "some updated volume_end"
    end

    test "update_bundle/2 with invalid data returns error changeset" do
      bundle = bundle_fixture()
      assert {:error, %Ecto.Changeset{}} = Bundles.update_bundle(bundle, @invalid_attrs)
      assert bundle == Bundles.get_bundle!(bundle.id)
    end

    test "delete_bundle/1 deletes the bundle" do
      bundle = bundle_fixture()
      assert {:ok, %Bundle{}} = Bundles.delete_bundle(bundle)
      assert_raise Ecto.NoResultsError, fn -> Bundles.get_bundle!(bundle.id) end
    end

    test "change_bundle/1 returns a bundle changeset" do
      bundle = bundle_fixture()
      assert %Ecto.Changeset{} = Bundles.change_bundle(bundle)
    end
  end
end

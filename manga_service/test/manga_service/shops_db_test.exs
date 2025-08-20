defmodule MangaService.ShopsDBTest do
  use MangaService.DataCase

  alias MangaService.ShopsDB

  describe "shops" do
    alias MangaService.ShopsDB.Shop

    import MangaService.ShopsDBFixtures

    @invalid_attrs %{store: nil, url: nil, condition: nil, price: nil, stock_status: nil, last_stock_update: nil, coupon: nil, is_on_sale: nil}

    test "list_shops/0 returns all shops" do
      shop = shop_fixture()
      assert ShopsDB.list_shops() == [shop]
    end

    test "get_shop!/1 returns the shop with given id" do
      shop = shop_fixture()
      assert ShopsDB.get_shop!(shop.id) == shop
    end

    test "create_shop/1 with valid data creates a shop" do
      valid_attrs = %{store: "some store", url: "some url", condition: "some condition", price: 120.5, stock_status: "some stock_status", last_stock_update: ~U[2024-11-02 20:51:00Z], coupon: "some coupon", is_on_sale: true}

      assert {:ok, %Shop{} = shop} = ShopsDB.create_shop(valid_attrs)
      assert shop.store == "some store"
      assert shop.url == "some url"
      assert shop.condition == "some condition"
      assert shop.price == 120.5
      assert shop.stock_status == "some stock_status"
      assert shop.last_stock_update == ~U[2024-11-02 20:51:00Z]
      assert shop.coupon == "some coupon"
      assert shop.is_on_sale == true
    end

    test "create_shop/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = ShopsDB.create_shop(@invalid_attrs)
    end

    test "update_shop/2 with valid data updates the shop" do
      shop = shop_fixture()
      update_attrs = %{store: "some updated store", url: "some updated url", condition: "some updated condition", price: 456.7, stock_status: "some updated stock_status", last_stock_update: ~U[2024-11-03 20:51:00Z], coupon: "some updated coupon", is_on_sale: false}

      assert {:ok, %Shop{} = shop} = ShopsDB.update_shop(shop, update_attrs)
      assert shop.store == "some updated store"
      assert shop.url == "some updated url"
      assert shop.condition == "some updated condition"
      assert shop.price == 456.7
      assert shop.stock_status == "some updated stock_status"
      assert shop.last_stock_update == ~U[2024-11-03 20:51:00Z]
      assert shop.coupon == "some updated coupon"
      assert shop.is_on_sale == false
    end

    test "update_shop/2 with invalid data returns error changeset" do
      shop = shop_fixture()
      assert {:error, %Ecto.Changeset{}} = ShopsDB.update_shop(shop, @invalid_attrs)
      assert shop == ShopsDB.get_shop!(shop.id)
    end

    test "delete_shop/1 deletes the shop" do
      shop = shop_fixture()
      assert {:ok, %Shop{}} = ShopsDB.delete_shop(shop)
      assert_raise Ecto.NoResultsError, fn -> ShopsDB.get_shop!(shop.id) end
    end

    test "change_shop/1 returns a shop changeset" do
      shop = shop_fixture()
      assert %Ecto.Changeset{} = ShopsDB.change_shop(shop)
    end
  end
end

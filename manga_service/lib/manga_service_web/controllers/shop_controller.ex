defmodule MangaServiceWeb.ShopController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.ShopsDB

  def index(conn, _params) do
    shops = ShopsDB.list_shops()

    json(
      conn,
      shops
      |> Enum.map(fn shop ->
        %{
          id: shop.id,
          item_id: shop.item_id,
          isbn: shop.isbn,
          store: shop.store,
          url: shop.url,
          condition: shop.condition,
          price: shop.price,
          stock_status: shop.stock_status,
          last_stock_update: shop.last_stock_update,
          coupon: shop.coupon,
          is_on_sale: shop.is_on_sale,
          promotion: shop.promotion,
          promotion_percentage: shop.promotion_percentage,
          backorder_details: shop.backorder_details,
          exclusive: shop.exclusive,
          is_bundle: shop.is_bundle,
          dropped_check: shop.dropped_check,
          inserted_at: shop.inserted_at,
          updated_at: shop.updated_at
        }
      end)
    )
  end

  def show(conn, %{"id" => item_id}) do
    shop = ShopsDB.get_shop_by_id!(item_id)

    case shop do
      nil ->
        raise "No record found for ID"

      _ ->
        json(conn, %{
          id: shop.id,
          item_id: shop.item_id,
          isbn: shop.isbn,
          store: shop.store,
          url: shop.url,
          condition: shop.condition,
          price: shop.price,
          stock_status: shop.stock_status,
          last_stock_update: shop.last_stock_update,
          coupon: shop.coupon,
          is_on_sale: shop.is_on_sale,
          promotion: shop.promotion,
          promotion_percentage: shop.promotion_percentage,
          backorder_details: shop.backorder_details,
          exclusive: shop.exclusive,
          is_bundle: shop.is_bundle,
          dropped_check: shop.dropped_check,
          inserted_at: shop.inserted_at,
          updated_at: shop.updated_at
        })
    end
  end

  def create(conn, %{"shop" => shop_params}) do
    case ShopsDB.create_shop(shop_params) do
      {:ok, shop} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: shop.id,
          item_id: shop.item_id,
          isbn: shop.isbn,
          store: shop.store,
          url: shop.url,
          condition: shop.condition,
          price: shop.price,
          stock_status: shop.stock_status,
          last_stock_update: shop.last_stock_update,
          coupon: shop.coupon,
          is_on_sale: shop.is_on_sale,
          promotion: shop.promotion,
          promotion_percentage: shop.promotion_percentage,
          backorder_details: shop.backorder_details,
          exclusive: shop.exclusive,
          is_bundle: shop.is_bundle,
          dropped_check: shop.dropped_check,
          inserted_at: shop.inserted_at,
          updated_at: shop.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => item_id, "shop" => shop_params}) do
    curr_shop = ShopsDB.get_shop_by_id!(item_id)

    case ShopsDB.update_shop(curr_shop, shop_params) do
      {:ok, shop} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: shop.id,
          item_id: shop.item_id,
          isbn: shop.isbn,
          store: shop.store,
          url: shop.url,
          condition: shop.condition,
          price: shop.price,
          stock_status: shop.stock_status,
          last_stock_update: shop.last_stock_update,
          coupon: shop.coupon,
          is_on_sale: shop.is_on_sale,
          promotion: shop.promotion,
          promotion_percentage: shop.promotion_percentage,
          backorder_details: shop.backorder_details,
          exclusive: shop.exclusive,
          is_bundle: shop.is_bundle,
          dropped_check: shop.dropped_check,
          inserted_at: shop.inserted_at,
          updated_at: shop.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => item_id}) do
    shop = ShopsDB.get_shop_by_id!(item_id)

    case ShopsDB.delete_shop(shop) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> text("Shop deleted")

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete shop"})
    end
  end
end
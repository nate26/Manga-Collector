defmodule MangaService.ShopsDB.Shop do
  use Ecto.Schema
  import Ecto.Changeset

  schema "shops" do
    field :item_id, :string
    field :isbn, :string
    field :store, :string
    field :url, :string
    field :condition, :string
    field :price, :float
    field :stock_status, :string
    field :last_stock_update, :utc_datetime
    field :coupon, :string
    field :is_on_sale, :boolean, default: false

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(shop, attrs) do
    shop
    |> cast(attrs, [:item_id, :isbn, :store, :condition, :url, :price, :stock_status, :last_stock_update, :coupon, :is_on_sale])
    |> validate_required([:item_id, :isbn, :store, :condition, :url, :price, :is_on_sale])
    |> unique_constraint(:item_id)
  end
end

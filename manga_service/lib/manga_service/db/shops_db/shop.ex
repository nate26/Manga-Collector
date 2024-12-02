defmodule MangaService.ShopsDB.Shop do
  use Ecto.Schema
  import Ecto.Changeset
  alias MangaService.{VolumesDB.Volume, MarketDB.Market}

  schema "shops" do
    field(:item_id, :string)
    field(:isbn, :string)
    field(:store, :string)
    field(:url, :string)
    field(:condition, :string)
    field(:price, :float)
    field(:stock_status, :string)
    field(:last_stock_update, :utc_datetime)
    field(:coupon, :string)
    field(:is_on_sale, :boolean, default: false)
    field(:promotion, :string)
    field(:promotion_percentage, :float)
    field(:backorder_details, :string)
    field(:exclusive, :boolean, default: false)
    field(:is_bundle, :boolean, default: false)
    field(:dropped_check, :boolean, default: false)

    belongs_to(:volume, Volume, references: :isbn, foreign_key: :isbn, define_field: false)
    belongs_to(:market, Market, references: :isbn, foreign_key: :isbn, define_field: false)

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(shop, attrs) do
    shop
    |> cast(attrs, [
      :item_id,
      :isbn,
      :store,
      :condition,
      :url,
      :price,
      :stock_status,
      :last_stock_update,
      :coupon,
      :is_on_sale,
      :promotion,
      :promotion_percentage,
      :backorder_details,
      :exclusive,
      :is_bundle,
      :dropped_check
    ])
    |> validate_required([
      :item_id,
      :isbn,
      :store,
      :condition,
      :url,
      :price,
      :is_on_sale,
      :exclusive,
      :is_bundle,
      :dropped_check
    ])
    |> unique_constraint(:item_id)
  end
end

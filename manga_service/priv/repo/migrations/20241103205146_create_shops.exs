defmodule MangaService.Repo.Migrations.CreateShops do
  use Ecto.Migration

  def change do
    create table(:shops) do
      add :item_id, :string
      add :isbn, :string
      add :store, :string
      add :condition, :string
      add :url, :string, size: 500
      add :price, :float
      add :stock_status, :string
      add :last_stock_update, :utc_datetime
      add :coupon, :string
      add :is_on_sale, :boolean, default: false, null: false
      add :promotion, :string
      add :promotion_percentage, :float
      add :backorder_details, :string
      add :exclusive, :boolean, default: false, null: false
      add :is_bundle, :boolean, default: false, null: false
      add :dropped_check, :boolean, default: false, null: false

      timestamps(type: :utc_datetime)
    end
    create unique_index(:shops, [:item_id])
  end
end

defmodule MangaService.Repo.Migrations.CreateBundles do
  use Ecto.Migration

  def change do
    create table(:bundles) do
      add(:item_id, :string)
      add(:series_id, :string)
      add(:shop_id, :string)
      add(:primary_cover_image, :string)
      add(:volumes, {:array, :map})
      add(:volume_start, :string)
      add(:volume_end, :string)
      add(:type, :string)

      timestamps(type: :utc_datetime)
    end

    create(unique_index(:bundles, [:item_id]))
  end
end

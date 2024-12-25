defmodule MangaService.Repo.Migrations.CreateVolumes do
  use Ecto.Migration

  def change do
    create table(:volumes) do
      add :isbn, :string
      add :brand, :string
      add :series, :string
      add :series_id, :string
      add :edition, :string
      add :edition_id, :string
      add :display_name, :string
      add :name, :string
      add :category, :string
      add :volume, :string
      add :url, :string, size: 500
      add :release_date, :date
      add :publisher, :string
      add :format, :string
      add :pages, :integer
      add :authors, :string
      add :isbn_10, :string
      add :primary_cover_image, :string, size: 500
      add :cover_images, {:array, :map}
      add :description, :string, size: 4095
      add :is_bundle, :boolean, default: false, null: false

      timestamps(type: :utc_datetime)
    end

    create unique_index(:volumes, [:isbn])
  end
end

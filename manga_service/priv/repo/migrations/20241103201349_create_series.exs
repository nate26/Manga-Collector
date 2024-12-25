defmodule MangaService.Repo.Migrations.CreateSeries do
  use Ecto.Migration

  def change do
    create table(:series) do
      add :series_id, :string
      add :title, :string
      add :associated_titles, {:array, :string}#, size: 1023
      add :url, :string, size: 500
      add :category, :string
      add :series_match_confidence, :decimal
      add :editions, {:array, :string}#, size: 1023
      add :volumes, {:array, :string}#, size: 2047
      add :description, :string, size: 8191
      add :cover_image, :string, size: 500
      add :genres, {:array, :string}
      add :themes, {:array, :map}#, size: 1023
      add :latest_chapter, :integer
      add :release_status, :string, size: 1023
      add :status, :string
      add :authors, {:array, :map}
      add :publishers, {:array, :map}
      add :bayesian_rating, :float
      add :rank, :integer
      add :recommendations, {:array, :string}

      timestamps(type: :utc_datetime)
    end
    create unique_index(:series, [:series_id])
  end
end

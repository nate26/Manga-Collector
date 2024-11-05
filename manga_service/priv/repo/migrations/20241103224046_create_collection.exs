defmodule MangaService.Repo.Migrations.CreateCollection do
  use Ecto.Migration

  def change do
    create table(:collection) do
      add :collection_id, :string
      add :user_id, :string
      add :isbn, :string
      add :collection, :string
      add :cost, :float
      add :store, :string
      add :purchase_date, :date
      add :read, :boolean, default: false, null: false
      add :tags, {:array, :string}, size: 500
      add :rating, :float

      timestamps(type: :utc_datetime)
    end
    create unique_index(:collection, [:collection_id])
  end
end

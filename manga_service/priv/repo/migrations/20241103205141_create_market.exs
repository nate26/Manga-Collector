defmodule MangaService.Repo.Migrations.CreateMarket do
  use Ecto.Migration

  def change do
    create table(:market) do
      add :isbn, :string
      add :retail_price, :float

      timestamps(type: :utc_datetime)
    end
    create unique_index(:market, [:isbn])
  end
end

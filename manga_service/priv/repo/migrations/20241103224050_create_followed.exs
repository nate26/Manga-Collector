defmodule MangaService.Repo.Migrations.CreateFollowed do
  use Ecto.Migration

  def change do
    create table(:followed) do
      add :user_id, :string
      add :follow_type, :string
      add :follow_id, :string

      timestamps(type: :utc_datetime)
    end
    create unique_index(:followed, [:user_id, :follow_id])
  end
end

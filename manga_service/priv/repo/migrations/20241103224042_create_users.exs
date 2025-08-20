defmodule MangaService.Repo.Migrations.CreateUsers do
  use Ecto.Migration

  def change do
    create table(:users) do
      add :username, :string
      add :email, :string
      add :password, :string
      add :user_id, :string
      add :picture, :string
      add :banner, :string
      add :color, :string
      add :theme, :string
      add :personal_stores, {:array, :string}, size: 500

      timestamps(type: :utc_datetime)
    end
    create unique_index(:users, [:email])
  end
end

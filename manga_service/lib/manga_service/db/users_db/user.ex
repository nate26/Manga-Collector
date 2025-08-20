defmodule MangaService.UsersDB.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :color, :string
    field :username, :string
    # field :password, MangaService.Encrypted.Binary
    field :email, :string
    field :user_id, :string
    field :picture, :string
    field :banner, :string
    field :theme, :string
    field :personal_stores, {:array, :string}

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:username, :email, :password, :user_id, :picture, :banner, :color, :theme, :personal_stores])
    |> validate_required([:username, :email, :password, :user_id, :personal_stores])
    |> unique_constraint(:email)
  end
end

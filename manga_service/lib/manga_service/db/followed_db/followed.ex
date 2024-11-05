defmodule MangaService.FollowedDB.Followed do
  use Ecto.Schema
  import Ecto.Changeset

  schema "followed" do
    field :user_id, :string
    field :follow_type, :string
    field :follow_id, :string

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(followed, attrs) do
    followed
    |> cast(attrs, [:user_id, :follow_type, :follow_id])
    |> validate_required([:user_id, :follow_type, :follow_id])
    |> unique_constraint([:user_id, :follow_id])
  end
end

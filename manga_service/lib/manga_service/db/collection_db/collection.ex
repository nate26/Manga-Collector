defmodule MangaService.CollectionDB.Collection do
  use Ecto.Schema
  import Ecto.Changeset

  schema "collection" do
    field :collection_id, :string
    field :read, :boolean, default: false
    field :store, :string
    field :collection, :string
    field :user_id, :string
    field :isbn, :string
    field :cost, :float
    field :purchase_date, :date
    field :tags, {:array, :string}
    field :rating, :float

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(collection, attrs) do
    collection
    |> cast(attrs, [:collection_id, :user_id, :isbn, :collection, :cost, :store, :purchase_date, :read, :tags, :rating])
    |> validate_required([:collection_id, :user_id, :isbn, :collection, :read, :tags])
    |> unique_constraint(:collection_id)
  end
end

defmodule MangaService.MarketDB.Market do
  use Ecto.Schema
  import Ecto.Changeset

  schema "market" do
    field :isbn, :string
    field :retail_price, :float

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(market, attrs) do
    market
    |> cast(attrs, [:isbn, :retail_price])
    |> validate_required([:isbn, :retail_price])
    |> unique_constraint(:isbn)
  end
end

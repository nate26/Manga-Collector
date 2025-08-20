defmodule MangaService.MarketDB do
  @moduledoc """
  The MarketDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.MarketDB.Market

  @doc """
  Returns the list of market.

  ## Examples

      iex> list_market()
      [%Market{}, ...]

  """
  def list_market do
    Repo.all(Market)
  end

  @doc """
  Gets a single market.

  Raises `Ecto.NoResultsError` if the Market does not exist.

  ## Examples

      iex> get_market!(123)
      %Market{}

      iex> get_market!(456)
      ** (Ecto.NoResultsError)

  """
  def get_market(id), do: Repo.get(Market, id)

  @doc """
  Gets a single volume market data by isbn.

  Raises `Ecto.NoResultsError` if the Market does not exist.

  ## Examples

      iex> get_market_by_isbn!("9781427816702")
      %Market{}

      iex> get_market_by_isbn!("9781427816702")
      ** (Ecto.NoResultsError)

  """
  def get_market_by_isbn(isbn), do: Repo.get_by(Market, %{isbn: isbn})

  @doc """
  Creates a market.

  ## Examples

      iex> create_market(%{field: value})
      {:ok, %Market{}}

      iex> create_market(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_market(attrs \\ %{}) do
    %Market{}
    |> Market.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a market.

  ## Examples

      iex> update_market(market, %{field: new_value})
      {:ok, %Market{}}

      iex> update_market(market, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_market(%Market{} = market, attrs) do
    market
    |> Market.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a market.

  ## Examples

      iex> delete_market(market)
      {:ok, %Market{}}

      iex> delete_market(market)
      {:error, %Ecto.Changeset{}}

  """
  def delete_market(%Market{} = market) do
    Repo.delete(market)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking market changes.

  ## Examples

      iex> change_market(market)
      %Ecto.Changeset{data: %Market{}}

  """
  def change_market(%Market{} = market, attrs \\ %{}) do
    Market.changeset(market, attrs)
  end
end

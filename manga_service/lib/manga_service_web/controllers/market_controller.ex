defmodule MangaServiceWeb.MarketController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.MarketDB

  def index(conn, _params) do
    markets = MarketDB.list_market()

    json(
      conn,
      markets
      |> Enum.map(fn market ->
        %{
          id: market.id,
          isbn: market.isbn,
          retail_price: market.retail_price,
          inserted_at: market.inserted_at,
          updated_at: market.updated_at
        }
      end)
    )
  end

  def show(conn, %{"id" => isbn}) do
    market = MarketDB.get_market_by_isbn(isbn)

    case market do
      nil ->
        raise "No record found for ISBN"

      _ ->
        json(conn, %{
          id: market.id,
          isbn: market.isbn,
          retail_price: market.retail_price,
          inserted_at: market.inserted_at,
          updated_at: market.updated_at
        })
    end
  end

  def create(conn, %{"market" => market_params}) do
    case MarketDB.create_market(market_params) do
      {:ok, market} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: market.id,
          isbn: market.isbn,
          retail_price: market.retail_price,
          inserted_at: market.inserted_at,
          updated_at: market.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => isbn, "market" => market_params}) do
    curr_market = MarketDB.get_market_by_isbn(isbn)

    case MarketDB.update_market(curr_market, market_params) do
      {:ok, market} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: market.id,
          isbn: market.isbn,
          retail_price: market.retail_price,
          inserted_at: market.inserted_at,
          updated_at: market.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => isbn}) do
    market = MarketDB.get_market_by_isbn(isbn)

    case MarketDB.delete_market(market) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> json(%{success: true})

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete market"})
    end
  end
end

defmodule MangaService.MarketDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.MarketDB` context.
  """

  @doc """
  Generate a market.
  """
  def market_fixture(attrs \\ %{}) do
    {:ok, market} =
      attrs
      |> Enum.into(%{
        isbn: "some isbn",
        retail_price: 120.5
      })
      |> MangaService.MarketDB.create_market()

    market
  end
end

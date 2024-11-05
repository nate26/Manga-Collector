defmodule MangaService.ShopsDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.ShopsDB` context.
  """

  @doc """
  Generate a shop.
  """
  def shop_fixture(attrs \\ %{}) do
    {:ok, shop} =
      attrs
      |> Enum.into(%{
        condition: "some condition",
        coupon: "some coupon",
        is_on_sale: true,
        last_stock_update: ~U[2024-11-02 20:51:00Z],
        price: 120.5,
        stock_status: "some stock_status",
        store: "some store",
        url: "some url"
      })
      |> MangaService.ShopsDB.create_shop()

    shop
  end
end

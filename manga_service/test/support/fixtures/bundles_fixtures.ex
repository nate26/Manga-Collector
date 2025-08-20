defmodule MangaService.BundlesFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.Bundles` context.
  """

  @doc """
  Generate a bundle.
  """
  def bundle_fixture(attrs \\ %{}) do
    {:ok, bundle} =
      attrs
      |> Enum.into(%{
        item_id: "some item_id",
        series_id: "some series_id",
        shop_id: "some shop_id",
        volume_end: "some volume_end",
        volume_start: "some volume_start",
        volumes: []
      })
      |> MangaService.Bundles.create_bundle()

    bundle
  end
end

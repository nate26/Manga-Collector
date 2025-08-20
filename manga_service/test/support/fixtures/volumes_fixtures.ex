defmodule MangaService.VolumesFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.Volumes` context.
  """

  @doc """
  Generate a volume.
  """
  def volume_fixture(attrs \\ %{}) do
    {:ok, volume} =
      attrs
      |> Enum.into(%{
        authors: "some authors",
        brand: "some brand",
        category: "some category",
        cover_images: [],
        description: "some description",
        display_name: "some display_name",
        edition: "some edition",
        edition_id: "some edition_id",
        format: "some format",
        isbn: "some isbn",
        isbn_10: "some isbn_10",
        name: "some name",
        pages: 42,
        primary_cover_image: "some primary_cover_image",
        publisher: "some publisher",
        record_added_date: ~N[2024-11-02 00:36:00],
        record_updated_date: ~N[2024-11-02 00:36:00],
        release_date: ~D[2024-11-02],
        series: "some series",
        series_id: "some series_id",
        url: "some url",
        volume: "some volume"
      })
      |> MangaService.Volumes.create_volume()

    volume
  end
end

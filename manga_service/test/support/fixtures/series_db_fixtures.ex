defmodule MangaService.SeriesDBFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `MangaService.SeriesDB` context.
  """

  @doc """
  Generate a series.
  """
  def series_fixture(attrs \\ %{}) do
    {:ok, series} =
      attrs
      |> Enum.into(%{
        associated_titles: ["option1", "option2"],
        authors: [],
        bayesian_rating: 120.5,
        category: "some category",
        cover_image: "some cover_image",
        description: "some description",
        editions: ["option1", "option2"],
        genres: ["option1", "option2"],
        latest_chapter: 42,
        publishers: [],
        rank: 42,
        recommendations: ["option1", "option2"],
        release_status: "some release_status",
        series_id: "some series_id",
        series_match_confidence: "120.5",
        status: "some status",
        themes: [],
        title: "some title",
        url: "some url",
        volumes: ["option1", "option2"]
      })
      |> MangaService.SeriesDB.create_series()

    series
  end
end

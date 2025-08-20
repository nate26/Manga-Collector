defmodule MangaService.SeriesDBTest do
  use MangaService.DataCase

  alias MangaService.SeriesDB

  describe "series" do
    alias MangaService.SeriesDB.Series

    import MangaService.SeriesDBFixtures

    @invalid_attrs %{status: nil, description: nil, title: nil, category: nil, url: nil, series_id: nil, associated_titles: nil, series_match_confidence: nil, editions: nil, volumes: nil, cover_image: nil, genres: nil, themes: nil, latest_chapter: nil, release_status: nil, authors: nil, publishers: nil, bayesian_rating: nil, rank: nil, recommendations: nil}

    test "list_series/0 returns all series" do
      series = series_fixture()
      assert SeriesDB.list_series() == [series]
    end

    test "get_series!/1 returns the series with given id" do
      series = series_fixture()
      assert SeriesDB.get_series!(series.id) == series
    end

    test "create_series/1 with valid data creates a series" do
      valid_attrs = %{status: "some status", description: "some description", title: "some title", category: "some category", url: "some url", series_id: "some series_id", associated_titles: ["option1", "option2"], series_match_confidence: "120.5", editions: ["option1", "option2"], volumes: ["option1", "option2"], cover_image: "some cover_image", genres: ["option1", "option2"], themes: [], latest_chapter: 42, release_status: "some release_status", authors: [], publishers: [], bayesian_rating: 120.5, rank: 42, recommendations: ["option1", "option2"]}

      assert {:ok, %Series{} = series} = SeriesDB.create_series(valid_attrs)
      assert series.status == "some status"
      assert series.description == "some description"
      assert series.title == "some title"
      assert series.category == "some category"
      assert series.url == "some url"
      assert series.series_id == "some series_id"
      assert series.associated_titles == ["option1", "option2"]
      assert series.series_match_confidence == Decimal.new("120.5")
      assert series.editions == ["option1", "option2"]
      assert series.volumes == ["option1", "option2"]
      assert series.cover_image == "some cover_image"
      assert series.genres == ["option1", "option2"]
      assert series.themes == []
      assert series.latest_chapter == 42
      assert series.release_status == "some release_status"
      assert series.authors == []
      assert series.publishers == []
      assert series.bayesian_rating == 120.5
      assert series.rank == 42
      assert series.recommendations == ["option1", "option2"]
    end

    test "create_series/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = SeriesDB.create_series(@invalid_attrs)
    end

    test "update_series/2 with valid data updates the series" do
      series = series_fixture()
      update_attrs = %{status: "some updated status", description: "some updated description", title: "some updated title", category: "some updated category", url: "some updated url", series_id: "some updated series_id", associated_titles: ["option1"], series_match_confidence: "456.7", editions: ["option1"], volumes: ["option1"], cover_image: "some updated cover_image", genres: ["option1"], themes: [], latest_chapter: 43, release_status: "some updated release_status", authors: [], publishers: [], bayesian_rating: 456.7, rank: 43, recommendations: ["option1"]}

      assert {:ok, %Series{} = series} = SeriesDB.update_series(series, update_attrs)
      assert series.status == "some updated status"
      assert series.description == "some updated description"
      assert series.title == "some updated title"
      assert series.category == "some updated category"
      assert series.url == "some updated url"
      assert series.series_id == "some updated series_id"
      assert series.associated_titles == ["option1"]
      assert series.series_match_confidence == Decimal.new("456.7")
      assert series.editions == ["option1"]
      assert series.volumes == ["option1"]
      assert series.cover_image == "some updated cover_image"
      assert series.genres == ["option1"]
      assert series.themes == []
      assert series.latest_chapter == 43
      assert series.release_status == "some updated release_status"
      assert series.authors == []
      assert series.publishers == []
      assert series.bayesian_rating == 456.7
      assert series.rank == 43
      assert series.recommendations == ["option1"]
    end

    test "update_series/2 with invalid data returns error changeset" do
      series = series_fixture()
      assert {:error, %Ecto.Changeset{}} = SeriesDB.update_series(series, @invalid_attrs)
      assert series == SeriesDB.get_series!(series.id)
    end

    test "delete_series/1 deletes the series" do
      series = series_fixture()
      assert {:ok, %Series{}} = SeriesDB.delete_series(series)
      assert_raise Ecto.NoResultsError, fn -> SeriesDB.get_series!(series.id) end
    end

    test "change_series/1 returns a series changeset" do
      series = series_fixture()
      assert %Ecto.Changeset{} = SeriesDB.change_series(series)
    end
  end
end

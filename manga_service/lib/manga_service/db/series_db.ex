defmodule MangaService.SeriesDB do
  @moduledoc """
  The SeriesDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.SeriesDB.Series

  @doc """
  Returns the list of series.

  ## Examples

      iex> list_series()
      [%Series{}, ...]

  """
  def list_series(params) do
    Series
    |> order_by(^filter_order_by(params["order_by"]))
    |> where(^filter_where(params))
    |> limit(^(params["limit"] || 100))
    |> offset(^(params["offset"] || 0))
    |> Repo.all()
    |> Repo.preload(:volumes)
  end

  defp filter_order_by("name_desc"),
    do: [desc: dynamic([_, v], v.display_name)]

  defp filter_order_by("name"),
    do: [asc: dynamic([_, v], v.display_name)]

  defp filter_order_by(_),
    do: []

  defp filter_where(params) do
    Enum.reduce(params, dynamic(true), fn
      {"title", value}, dynamic ->
        dynamic(
          [s],
          ^dynamic and fragment("lower(?) like '%' || lower(?) || '%'", s.title, ^value)
        )

      {_, _}, dynamic ->
        dynamic
    end)
  end

  @doc """
  Gets a single series.

  Raises `Ecto.NoResultsError` if the Series does not exist.

  ## Examples

      iex> get_series!(123)
      %Series{}

      iex> get_series!(456)
      ** (Ecto.NoResultsError)

  """
  def get_series(id), do: Repo.get(Series, id) |> Repo.preload(:volumes)

  @doc """
  Gets a single series by series_id.

  Raises `Ecto.NoResultsError` if the Series does not exist.

  ## Examples

      iex> get_series_by_id!("id")
      %Series{}

      iex> get_series_by_id!("")
      ** (Ecto.NoResultsError)

  """
  def get_series_by_id(series_id),
    do: Repo.get_by(Series, %{series_id: series_id}) |> Repo.preload(:volumes)

  @doc """
  Creates a series.

  ## Examples

      iex> create_series(%{field: value})
      {:ok, %Series{}}

      iex> create_series(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_series(attrs \\ %{}) do
    %Series{}
    |> Series.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a series.

  ## Examples

      iex> update_series(series, %{field: new_value})
      {:ok, %Series{}}

      iex> update_series(series, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_series(%Series{} = series, attrs) do
    series
    |> Series.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a series.

  ## Examples

      iex> delete_series(series)
      {:ok, %Series{}}

      iex> delete_series(series)
      {:error, %Ecto.Changeset{}}

  """
  def delete_series(%Series{} = series) do
    Repo.delete(series)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking series changes.

  ## Examples

      iex> change_series(series)
      %Ecto.Changeset{data: %Series{}}

  """
  def change_series(%Series{} = series, attrs \\ %{}) do
    Series.changeset(series, attrs)
  end

  def distinct_genres do
    # query = from(o in Project.Orders.Schemas.Order, where:
    # fragment("(select count(distinct json->> 'customer_id') from unnest(?) as json)",  o.invoices) >1)

    # from(
    #   series in Series,
    #   where:
    #     fragment(
    #       "(select count(distinct json->> 'genres') from unnest(?) as json)",
    #       series.genres
    #     ) > 1
    # )
    # from(
    #   series in Series,
    #   where: fragment("select distinct(genres) from unnest(?)", series.genres)
    # )
    # query =
    #   Repo.all(fragment("select distinct(unnest(genres)) from series"))
  end
end

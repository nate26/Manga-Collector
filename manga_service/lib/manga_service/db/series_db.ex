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

    # |> Repo.preload(:volume_details)
  end

  defp filter_order_by("title_desc"),
    do: [desc: dynamic([s], s.title)]

  defp filter_order_by("title"),
    do: [asc: dynamic([s], s.title)]

  defp filter_order_by(_),
    do: []

  defp filter_where(params) do
    Enum.reduce(params, dynamic(true), fn
      {"title", value}, dynamic ->
        dynamic(
          [s],
          # TODO include associated titles
          ^dynamic and fragment("lower(?) like '%' || lower(?) || '%'", s.title, ^value)
        )

      {"status", value}, dynamic ->
        dynamic([s], ^dynamic and s.status == ^value)

      {"category", value}, dynamic ->
        dynamic([s], ^dynamic and s.category == ^value)

      {"genre", value}, dynamic ->
        dynamic(
          [s],
          ^dynamic and fragment("? = Any(?)", ^value, s.genres)
        )

      {"theme", value}, dynamic ->
        dynamic(
          [s],
          ^dynamic and
            fragment(
              "? = ANY(select element ->> 'theme' from unnest(?) as element)",
              ^value,
              s.themes
            )
        )

      {"author", value}, dynamic ->
        dynamic(
          [s],
          ^dynamic and
            fragment(
              "? = ANY(select element ->> 'name' from unnest(?) as element)",
              ^value,
              s.authors
            )
        )

      {"publisher", value}, dynamic ->
        dynamic(
          [s],
          ^dynamic and
            fragment(
              "? = ANY(select element ->> 'name' from unnest(?) as element)",
              ^value,
              s.publishers
            )
        )

      {"rank_le", value}, dynamic ->
        dynamic([s], ^dynamic and s.rank <= ^value)

      {"rank_ge", value}, dynamic ->
        dynamic([s], ^dynamic and s.rank >= ^value)

      {"rating_le", value}, dynamic ->
        dynamic([s], ^dynamic and s.bayesian_rating <= ^value)

      {"rating_ge", value}, dynamic ->
        dynamic([s], ^dynamic and s.bayesian_rating >= ^value)

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
  def get_series(id), do: Repo.get(Series, id) |> Repo.preload(:volume_details)

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
    do: Repo.get_by(Series, %{series_id: series_id}) |> Repo.preload(:volume_details)

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

  def distinct_status do
    Repo.all(from(v in Series, select: v.status, distinct: true, where: not is_nil(v.status)))
  end

  def distinct_category do
    Repo.all(from(v in Series, select: v.category, distinct: true, where: not is_nil(v.category)))
  end

  def distinct_genres do
    Ecto.Adapters.SQL.query!(
      Repo,
      "select distinct(genre) from series, unnest(genres) as genre order by genre"
    ).rows
    |> List.flatten()
  end

  def distinct_themes do
    Ecto.Adapters.SQL.query!(
      Repo,
      "select distinct(element ->> 'theme') as theme from series, unnest(themes) as element order by theme"
    ).rows
    |> List.flatten()
  end

  def distinct_authors do
    Ecto.Adapters.SQL.query!(
      Repo,
      "select distinct(element ->> 'name') as author from series, unnest(authors) as element order by author"
    ).rows
    |> List.flatten()
  end

  def distinct_publishers do
    Ecto.Adapters.SQL.query!(
      Repo,
      "select distinct(element ->> 'name') as publisher from series, unnest(publishers) as element order by publisher"
    ).rows
    |> List.flatten()
  end
end

defmodule MangaService.VolumesDB do
  @moduledoc """
  The Volumes context.
  """

  import Ecto.Query, only: [from: 2], warn: false
  alias MangaService.Repo

  alias MangaService.VolumesDB.Volume

  def parse_integer!(string) do
    case Integer.parse(string || "0") do
      {number, _} -> number
      :error -> 0
    end
  end

  @doc """
  Returns the list of volumes.

  ## Examples

      iex> list_volumes()
      [%Volume{}, ...]

  """
  def list_volumes do
    Repo.all(Volume)
  end

  @doc """
  Returns the list of volumes.

  ## Examples

      iex> list_volumes()
      [%Volume{}, ...]

  """
  def list_volumes_in_series(series_id, limit, offset) do
    limit =
      case parse_integer!(limit) do
        l when not is_number(l) or l <= 0 or l > 100 -> 100
        l -> l
      end

    offset = parse_integer!(offset)

    query =
      case series_id do
        "none" ->
          from(v in Volume,
            where: is_nil(v.series_id),
            order_by: [asc: v.release_date],
            limit: ^limit,
            offset: ^offset,
            select: v
          )

        "" ->
          from(v in Volume,
            order_by: [asc: v.release_date],
            limit: ^limit,
            offset: ^offset,
            select: v
          )

        _ ->
          from(v in Volume,
            where: v.series_id == ^series_id,
            order_by: [asc: v.release_date],
            limit: ^limit,
            offset: ^offset,
            select: v
          )
      end

    Repo.all(query)
  end

  @doc """
  Gets a single volume.

  Raises `Ecto.NoResultsError` if the Volume does not exist.

  ## Examples

      iex> get_volume!(123)
      %Volume{}

      iex> get_volume!(456)
      ** (Ecto.NoResultsError)

  """
  def get_volume(id), do: Repo.get(Volume, id)

  @doc """
  Gets a single volume by isbn.

  Raises `Ecto.NoResultsError` if the Volume does not exist.

  ## Examples

      iex> get_volume_by_isbn!("9781427816702")
      %Volume{}

      iex> get_volume_by_isbn!("9781427816702")
      ** (Ecto.NoResultsError)

  """
  def get_volume_by_isbn(isbn) do
    Volume
    |> Repo.get_by(%{isbn: isbn})
    |> Repo.preload([:market_data, :series_data])
  end

  @doc """
  Creates a volume.

  ## Examples

      iex> create_volume(%{field: value})
      {:ok, %Volume{}}

      iex> create_volume(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_volume(attrs \\ %{}) do
    %Volume{}
    |> Volume.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a volume.

  ## Examples

      iex> update_volume(volume, %{field: new_value})
      {:ok, %Volume{}}

      iex> update_volume(volume, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_volume(%Volume{} = volume, attrs) do
    volume
    |> Volume.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a volume.

  ## Examples

      iex> delete_volume(volume)
      {:ok, %Volume{}}

      iex> delete_volume(volume)
      {:error, %Ecto.Changeset{}}

  """
  def delete_volume(%Volume{} = volume) do
    Repo.delete(volume)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking volume changes.

  ## Examples

      iex> change_volume(volume)
      %Ecto.Changeset{data: %Volume{}}

  """
  def change_volume(%Volume{} = volume, attrs \\ %{}) do
    Volume.changeset(volume, attrs)
  end
end

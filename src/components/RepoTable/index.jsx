import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import RepoRow from "../RepoRow";

import repoData from "../../../data/data.json";

function RepoTable({ reposData = [] }) {
  const repoList = repoData
    .map((repo) => {
      return {
        name: repo.name,
        commits: repo.commits,
        stars: repo.total_stars,
        contributors: repo.contributors,
      };
    })
    .sort((a, b) => {
      return b.stars - a.stars;
    });

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell>Repo name</TableCell>
            <TableCell align="right">Stars</TableCell>
            <TableCell align="right"># of commits</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {repoList.map((row) => (
            <RepoRow row={row} key={row.name} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default RepoTable;

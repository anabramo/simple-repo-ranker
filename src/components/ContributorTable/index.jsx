import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

function ContributorTable({ contributors = [] }) {
  return (
    <Table size="small" aria-label="purchases">
      <TableHead>
        <TableRow>
          <TableCell>Login</TableCell>
          <TableCell align="right"># of commits</TableCell>
          <TableCell align="right"># of PRs</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {contributors.map((contributor) => (
          <TableRow key={contributor.id}>
            <TableCell component="th" scope="row">
              {contributor.id}
            </TableCell>
            <TableCell align="right">{contributor.commits}</TableCell>
            <TableCell align="right">{contributor.PRs ?? "-"}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

export default ContributorTable;

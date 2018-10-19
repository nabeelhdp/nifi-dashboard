
%# disp_table.tpl

<p>The items are as follows:</p>
<table border="1">
  <tr>
      <th>"Processor Group ID"</th>
      <th>"Processor Group Name"</th>
      <th>"Bytes Queued"</th>
  </tr>
  %for key, value in sorted(dataparam.iteritems(), reverse = True, key=lambda (k,v): (v,k)):
    <tr>
        <td>{{key}} </td>
        <td>{{pgnames[key]}} </td>
        <td>{{value}} </td>
    </tr>
  %end
</table>

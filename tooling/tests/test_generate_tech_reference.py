import json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import generate_tech_reference as g


class TestInject(unittest.TestCase):
    def test_replaces_marked_region_and_keeps_markers(self):
        md = "Intro\n<!-- GENERATED:schema -->\nOLD\n<!-- /GENERATED:schema -->\nOutro\n"
        out = g.inject(md, {"schema": "NEW TABLE"})
        self.assertIn("<!-- GENERATED:schema -->", out)
        self.assertIn("<!-- /GENERATED:schema -->", out)
        self.assertIn("NEW TABLE", out)
        self.assertNotIn("OLD", out)
        self.assertTrue(out.startswith("Intro"))
        self.assertTrue(out.rstrip().endswith("Outro"))

    def test_leaves_unmatched_sections_untouched(self):
        md = "<!-- GENERATED:schema -->\nX\n<!-- /GENERATED:schema -->\n"
        out = g.inject(md, {"domains": "Y"})
        self.assertIn("X", out)


class TestRender(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()
        exp = os.path.join(self.dir, "json_export_test")
        os.makedirs(os.path.join(exp, "svc1_Demo_Service", "layers"))
        with open(os.path.join(exp, "_manifest.json"), "w") as f:
            json.dump({"portal": "https://p/", "items": [
                {"id": "svc1", "title": "Demo Service", "type": "Feature Service", "source": "requested"}
            ]}, f)
        with open(os.path.join(exp, "svc1_Demo_Service", "layers", "0_Demo_Layer.json"), "w") as f:
            json.dump({"name": "Demo Layer", "type": "Feature Layer", "fields": [
                {"name": "status", "alias": "Status", "type": "esriFieldTypeString", "length": 50,
                 "nullable": True, "editable": True,
                 "domain": {"type": "codedValue", "name": "d_status",
                            "codedValues": [{"name": "Open"}, {"name": "Closed"}]}}
            ], "relationships": [{"name": "Demo_Rel", "cardinality": "esriRelCardinalityOneToMany"}]}, f)
        self.export = g.load_export(exp)

    def test_load_export_reads_items_and_layers(self):
        self.assertEqual(len(self.export["items"]), 1)
        self.assertIn("svc1", self.export["layers"])

    def test_render_sections_has_all_keys_and_content(self):
        s = g.render_sections(self.export)
        for k in ("portal-items", "services", "schema", "domains", "subtypes", "relationships"):
            self.assertIn(k, s)
        self.assertIn("Demo Service", s["portal-items"])
        self.assertIn("Status", s["schema"])
        self.assertIn("Open", s["domains"])
        self.assertIn("Demo_Rel", s["relationships"])

    def test_render_sections_deduplicates_relationship_rows(self):
        import json, os, tempfile
        d = tempfile.mkdtemp()
        exp = os.path.join(d, "json_export_dedup")
        os.makedirs(os.path.join(exp, "svc2_Dup_Service", "layers"))
        with open(os.path.join(exp, "_manifest.json"), "w") as f:
            json.dump({"portal": "https://p/", "items": [
                {"id": "svc2", "title": "Dup Service", "type": "Feature Service", "source": "test"}
            ]}, f)
        with open(os.path.join(exp, "svc2_Dup_Service", "layers", "0_Dup_Layer.json"), "w") as f:
            json.dump({"name": "Dup Layer", "type": "Feature Layer", "fields": [], "relationships": [
                {"name": "Demo_Rel", "cardinality": "esriRelCardinalityOneToMany"},
                {"name": "Demo_Rel", "cardinality": "esriRelCardinalityOneToMany"}
            ]}, f)
        export = g.load_export(exp)
        s = g.render_sections(export)
        self.assertEqual(s["relationships"].count("Demo_Rel"), 1)

    def test_group_layers_have_no_field_table_and_nest_children(self):
        import json, os, tempfile
        d = tempfile.mkdtemp()
        exp = os.path.join(d, "json_export_group")
        os.makedirs(os.path.join(exp, "svcM_Map_Service", "layers"))
        with open(os.path.join(exp, "_manifest.json"), "w") as f:
            json.dump({"items": [
                {"id": "svcM", "title": "Map Svc", "type": "Map Service", "source": "referenced"}
            ]}, f)
        # Group layer (id 14) with one child (id 10) that has fields.
        with open(os.path.join(exp, "svcM_Map_Service", "layers", "14_Group.json"), "w") as f:
            json.dump({"id": 14, "name": "Tracking By Period", "type": "Group Layer",
                       "parentLayer": None, "subLayers": [{"id": 10, "name": "Child A"}],
                       "fields": []}, f)
        with open(os.path.join(exp, "svcM_Map_Service", "layers", "10_ChildA.json"), "w") as f:
            json.dump({"id": 10, "name": "Child A", "type": "Feature Layer",
                       "parentLayer": {"id": 14, "name": "Tracking By Period"}, "subLayers": [],
                       "fields": [{"name": "foo", "alias": "Foo", "type": "esriFieldTypeString"}]}, f)
        s = g.render_sections(g.load_export(exp))["schema"]
        # Group appears as a heading and is marked as a container, with no field table.
        self.assertIn("Tracking By Period (Group Layer)", s)
        self.assertIn("Group layer", s)
        # Exactly one field table (the child's) — the group did NOT get one.
        self.assertEqual(s.count("| Field | Alias |"), 1)
        # Child is nested one heading level deeper (##### under the #### group).
        self.assertIn("##### Child A", s)
        self.assertIn("Foo", s)


if __name__ == "__main__":
    unittest.main()

# Weeds & Invasives Treatment Application — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

The Weeds & Invasives Treatment Application is a three-component GIS solution built by KCI for the Solano County Agriculture Department (late 2022 – mid 2023). The components are:

1. **Survey123 form — "Weeds and Invasives Treatment Application"** (item `5b176ab3af244d3d8b8add5c19184dbf`): The primary data-collection tool. A single form record follows the treatment lifecycle through all stages via the Survey123 Inbox. The form is launched from the Parcels REGIS pop-up hyperlink in Field Maps or the web app, which passes parcel attributes (Parcel ID, assessee name, address, site number, road, city, and parcel address) into the form using the `arcgis-survey123://` deep-link protocol. The form points to an SDE-backed feature service (not the Survey123-managed hosted service).

   The Parcels REGIS pop-up hyperlink structure is:

   ```text
   arcgis-survey123://?itemID=5b176ab3af244d3d8b8add5c19184dbf
     &field:treatment_parcelid={parcelid}
     &field:treatment_assessee={assessee}
     &field:treatment_assessee_addr1={addr1}
     &field:treatment_assessee_addr2={addr2}
     &field:treatment_assessee_addr3={addr3}
     &field:treatment_assessee_addr_zip={addrzip}
     &field:treatment_sitenum={sitenum}
     &field:treatment_siteroad={siteroad}
     &field:treatment_sitecity={sitecity}
     &field:treatment_parcel_addr={parceladdress}
   ```

2. **Field Maps web map — "Weeds and Invasives – Tracking and Field Map"** (item `ae9facb1a73047f7b2d39a3940fd5e4a`): Used in Esri Field Maps on mobile devices and tablets, and in the web application for parcel selection. Contains the Parcels REGIS layer (with the Survey123 launch hyperlink), WI Treatment Tracking Points, WI Treatment Points (Survey123 submissions), and WI Treatment Areas.

3. **Web AppBuilder app — "Weeds and Invasives Treatment App – Tracking and Field Data"** (item `f2be7959bdfc4c77b30ebbefc9829987`): Desktop tracking and editing application. Widgets include Search, Select, Edit, Legend, Layer List, Basemap Gallery, and Bookmarks. Attribute editing of Survey123-sourced points and areas is disabled in this app to prevent conflicts with the Survey123 record; only geometry editing and tracking-point attribute editing are enabled.

Data is stored in the enterprise PostgreSQL **"agdept"** database and published as referenced (not hosted) feature services.

## 2. Portal Items

<!-- GENERATED:portal-items -->
| Title | Type | Source | Item ID |
|---|---|---|---|
| Weeds and Invasives Treatment App - Tracking and Field Data | Web Mapping Application | requested | f2be7959bdfc4c77b30ebbefc9829987 |
| Weeds and Invasives - Tracking and Field Map | Web Map | requested | ae9facb1a73047f7b2d39a3940fd5e4a |
| Weeds and Invasives Treatment Application | Form | referenced | 5b176ab3af244d3d8b8add5c19184dbf |
| World Topographic Map | Vector Tile Service | referenced | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| WI Treatment Tracking | Feature Service | referenced | cf6f3e7fbb5c4e6580af1c82a9ef16b9 |
| WI Treatment Application S123 | Feature Service | referenced | f7482b33ef0f423db0b1a1ff31a93fd2 |
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

All data services for this solution are **referenced** (not hosted): they are published from an ArcGIS Pro project that reads directly from the PostgreSQL "agdept" enterprise geodatabase SDE. The ArcGIS Pro project is located at:

```text
E:\ServiceUpdates\AgInspectionTool\W&I Treatment App
```

The Survey123 form was published initially using ArcGIS Survey123 Connect, which created the hosted feature service. The data was then exported as a File Geodatabase, loaded into the agdept SDE, and the service was re-published from ArcGIS Pro pointing to the SDE-backed datasets. The Survey123 form's Excel spreadsheet was then updated with the correct submission URL and republished in Survey123 Connect.

**Archiving and sync are enabled** on all four datasets (`wi_treatment_tracking`, `wi_treatmentpoints`, `wi_r_treatment_areas`, `wi_r_files`) to support the offline workflow in Field Maps and to enable edit tracking on `wi_treatmentpoints`. Note: the edit-tracking capability was not in the original project scope; database views surfacing stage-change history are documented as a future option.

The Survey123 Connect source files are located at:

```text
E:\ServiceUpdates\AgInspectionTool\Weeds and Invasives Treatment Application Survey123 Connect Files.zip
```

The generated table below reflects the portal items captured in the JSON export for this solution.

<!-- GENERATED:services -->
| Service / Item | Type | Item ID |
|---|---|---|
| World Topographic Map | Vector Tile Service | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| WI Treatment Tracking | Feature Service | cf6f3e7fbb5c4e6580af1c82a9ef16b9 |
| WI Treatment Application S123 | Feature Service | f7482b33ef0f423db0b1a1ff31a93fd2 |
<!-- /GENERATED:services -->

## 4. Database Schema

<!-- GENERATED:schema -->
#### WI - Treatment Tracking (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| observ_confirm | Observation Confirmed | String | 15 | True | True | wi_Yes_No_Etc |
| assess_approval_rec | Assessee Approval Received | String | 15 | True | True | wi_Yes_No_Etc |
| tenant_approval_rec | Tenant Approval Received | String | 15 | True | True | wi_Yes_No_Etc |
| follow_up_date | Follow Up Date | Date | 8 | True | True |  |
| post_ver_date | Post Verification Date | Date | 8 | True | True |  |
| treat_appr_comm | Treatment Comment | String | 255 | True | True |  |
| treatment_stage | Treatment Stage | String | 30 | True | True | wi_treatment_stage |
| ready_to_treat | Ready to Treat | String | 5 | True | True | yes no |
| treatment_complete | Treatment Complete Date | Date | 8 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### wi_treatmentpoints (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| form_start | form_start | Date | 8 | True | True |  |
| form_end | form_end | Date | 8 | True | True |  |
| fo_s123_username | fo_s123_username | String | 255 | True | True |  |
| form_version | Form Version | String | 255 | True | True |  |
| treatment_assessee | Assessee | String | 255 | True | True |  |
| treatment_assessee_addr1 | Assessee Address 1 | String | 255 | True | True |  |
| treatment_assessee_addr2 | Assessee Address 2 | String | 255 | True | True |  |
| treatment_assessee_addr3 | Assessee Address 3 | String | 255 | True | True |  |
| treatment_assessee_addr_zip | Assessee Zip | String | 255 | True | True |  |
| treatment_assessee_addr | Assessee Address (Combined) | String | 255 | True | True |  |
| treatment_assessee_comm | Assessee Comments | String | 255 | True | True |  |
| treatment_sitenum | Site Number | String | 255 | True | True |  |
| treatment_siteroad | Site Road | String | 255 | True | True |  |
| treatment_sitecity | Site City | String | 255 | True | True |  |
| treatment_parcel_addr | Site/Parcel Address | String | 255 | True | True |  |
| treatment_parcelid | Site Parcel ID | String | 255 | True | True |  |
| treatment_site_comm | Treatment/Site Comments | String | 255 | True | True |  |
| treatment_lat | Latitude | Double |  | True | True |  |
| treatment_long | Longitude | Double |  | True | True |  |
| horaccmeters | Accuracy | Double |  | True | True |  |
| calfloraid | Calflora ID | String | 255 | True | True |  |
| scientificname | Scientific Name | String | 255 | True | True | wi_scientificname |
| commonname | Common Name | String | 255 | True | True |  |
| scientificname_oth | Scientific Name (Other) | String | 255 | True | True |  |
| commonname_otth | Common Name (Other) | String | 255 | True | True |  |
| treatment_stage | Stage | String | 255 | True | True | wi_treatment_stage |
| projected_revisit_post_ver | Projected Revisit / "Post Verification" Date | Date | 8 | True | True |  |
| initial_obv_date_time | Initial Observation Date/Time | Date | 8 | True | True |  |
| initial_obv_observer | Initial Observation Observer(s) | String | 255 | True | True |  |
| initial_obv_confirmed | Initial Observation Confirmed? | String | 255 | True | True | wi_yes_no |
| initial_obv_comm | Initial Observation Comment | String | 255 | True | True |  |
| initial_confirm_approval | Approval Confirmation | String | 255 | True | True | wi_initial_confirm_approval |
| initial_treat_date_time | Initial Treatment Date/Time | Date | 8 | True | True |  |
| initial_treat_observer | Initial Treatment Observer(s) | String | 255 | True | True |  |
| initial_treat | Initial Treatment | String | 255 | True | True | wi_yes_no |
| initial_treat_num | Initial Treatment Number | Integer |  | True | True |  |
| initial_treat_comm | Initial Treatment Comment | String | 255 | True | True |  |
| initial_treat_result | Initial Treatment Result | String | 255 | True | True | wi_yes_no |
| followup_treat_date_time | Follow Up Treatment Date/Time | Date | 8 | True | True |  |
| followup_treat_observer | Follow Up Treatment Observer(s) | String | 255 | True | True |  |
| followup_treatment | Follow Up Treatment | String | 255 | True | True | wi_yes_no |
| followup_treat_comm | Follow Up Treatment Comment | String | 255 | True | True |  |
| postver_date_time | Post Treatment Verification Date/Time | Date | 8 | True | True |  |
| postver_observer | Post Treatment Verification Observer(s) | String | 255 | True | True |  |
| postver_complete | Post Treatment Verification Complete | String | 255 | True | True | wi_yes_no |
| postver_comm | Post Treatment Verification Comment | String | 255 | True | True |  |
| created_date | created_date | Date | 8 | True | False |  |
| created_user | created_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |

#### wi_r_treatment_areas (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parentglobalid | ParentGlobalID | GUID | 38 | True | True |  |
| created_date | created_date | Date | 8 | True | False |  |
| created_user | created_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |

#### wi_r_files (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| file_stage | Treatment Stage | String | 255 | True | True | wi_treatment_file_stage |
| parentglobalid | ParentGlobalID | GUID | 38 | True | True |  |
| created_date | created_date | Date | 8 | True | False |  |
| created_user | created_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
**wi_Yes_No_Etc**

| Coded Value | Alias |
|---|---|
| Yes | Yes |
| No | No |
| N/A | N/A |
| Pending | Pending |
| Refused | Refused |

**wi_initial_confirm_approval**

| Coded Value | Alias |
|---|---|
| Yes | Yes |
| No | No |
| N/A | N/A |
| Pending | Pending |
| Refused | Refused |

**wi_scientificname**

| Coded Value | Alias |
|---|---|
| Abutilon theophrasti | Abutilon theophrasti |
| Acacia dealbata | Acacia dealbata |
| Acacia longifolia | Acacia longifolia |
| Acacia melanoxylon | Acacia melanoxylon |
| Acacia paradoxa | Acacia paradoxa |
| Acaena californica | Acaena californica |
| Acer macrophyllum | Acer macrophyllum |
| Acer negundo | Acer negundo |
| Achillea millefolium | Achillea millefolium |
| Achyrachaena mollis | Achyrachaena mollis |
| Acmispon americanus | Acmispon americanus |
| Acmispon americanus var. americanus | Acmispon americanus var. americanus |
| Acmispon brachycarpus | Acmispon brachycarpus |
| Acmispon denticulatus | Acmispon denticulatus |
| Acmispon glaber | Acmispon glaber |
| Acmispon glaber var. glaber | Acmispon glaber var. glaber |
| Acmispon grandiflorus | Acmispon grandiflorus |
| Acmispon grandiflorus var. grandiflorus | Acmispon grandiflorus var. grandiflorus |
| Acmispon micranthus | Acmispon micranthus |
| Acmispon parviflorus | Acmispon parviflorus |
| Acmispon strigosus | Acmispon strigosus |
| Acmispon wrangelianus | Acmispon wrangelianus |
| Adelinia grandis | Adelinia grandis |
| Adenostoma fasciculatum | Adenostoma fasciculatum |
| Adiantum aleuticum | Adiantum aleuticum |
| Adiantum jordanii | Adiantum jordanii |
| Aegilops triuncialis | Aegilops triuncialis |
| Aesculus californica | Aesculus californica |
| Agastache urticifolia | Agastache urticifolia |
| Agave americana | Agave americana |
| Agoseris apargioides | Agoseris apargioides |
| Agoseris aurantiaca | Agoseris aurantiaca |
| Agoseris grandiflora | Agoseris grandiflora |
| Agoseris grandiflora var. grandiflora | Agoseris grandiflora var. grandiflora |
| Agoseris heterophylla | Agoseris heterophylla |
| Agoseris heterophylla var. heterophylla | Agoseris heterophylla var. heterophylla |
| Agrostis avenacea | Agrostis avenacea |
| Agrostis capillaris | Agrostis capillaris |
| Agrostis exarata | Agrostis exarata |
| Agrostis gigantea | Agrostis gigantea |
| Agrostis hallii | Agrostis hallii |
| Agrostis hendersonii | Agrostis hendersonii |
| Agrostis microphylla | Agrostis microphylla |
| Agrostis pallens | Agrostis pallens |
| Agrostis stolonifera | Agrostis stolonifera |
| Agrostis tandilensis | Agrostis tandilensis |
| Ailanthus altissima | Ailanthus altissima |
| Aira caryophyllea | Aira caryophyllea |
| Aira elegans | Aira elegans |
| Albizia julibrissin | Albizia julibrissin |
| Alcea rosea | Alcea rosea |
| Alisma lanceolatum | Alisma lanceolatum |
| Alisma triviale | Alisma triviale |
| Allium amplectens | Allium amplectens |
| Allium crispum | Allium crispum |
| Allium neapolitanum | Allium neapolitanum |
| Allium paniculatum | Allium paniculatum |
| Allium serra | Allium serra |
| Allium triquetrum | Allium triquetrum |
| Allium unifolium | Allium unifolium |
| Allophyllum divaricatum | Allophyllum divaricatum |
| Allophyllum gilioides | Allophyllum gilioides |
| Allophyllum gilioides ssp. gilioides | Allophyllum gilioides ssp. gilioides |
| Allophyllum gilioides ssp. violaceum | Allophyllum gilioides ssp. violaceum |
| Alnus rhombifolia | Alnus rhombifolia |
| Alopecurus saccatus | Alopecurus saccatus |
| Alternanthera philoxeroides | Alternanthera philoxeroides |
| Amaranthus albus | Amaranthus albus |
| Amaranthus blitoides | Amaranthus blitoides |
| Amaranthus californicus | Amaranthus californicus |
| Amaranthus caudatus | Amaranthus caudatus |
| Amaranthus hybridus | Amaranthus hybridus |
| Amaranthus hypochondriacus | Amaranthus hypochondriacus |
| Amaranthus powellii | Amaranthus powellii |
| Amaranthus retroflexus | Amaranthus retroflexus |
| Amaryllis belladonna | Amaryllis belladonna |
| Ambrosia psilostachya | Ambrosia psilostachya |
| Ammannia coccinea | Ammannia coccinea |
| Ammannia robusta | Ammannia robusta |
| Ammi majus | Ammi majus |
| Ammi visnaga | Ammi visnaga |
| Amsinckia douglasiana | Amsinckia douglasiana |
| Amsinckia eastwoodiae | Amsinckia eastwoodiae |
| Amsinckia intermedia | Amsinckia intermedia |
| Amsinckia lycopsoides | Amsinckia lycopsoides |
| Amsinckia menziesii | Amsinckia menziesii |
| Amsinckia retrorsa | Amsinckia retrorsa |
| Amsinckia spectabilis | Amsinckia spectabilis |
| Ancistrocarphus filagineus | Ancistrocarphus filagineus |
| Andropogon glomeratus | Andropogon glomeratus |
| Anemopsis californica | Anemopsis californica |
| Angelica californica | Angelica californica |
| Angelica tomentosa | Angelica tomentosa |
| Anisodontea capensis | Anisodontea capensis |
| Anredera cordifolia | Anredera cordifolia |
| Anthemis cotula | Anthemis cotula |
| Anthoxanthum odoratum | Anthoxanthum odoratum |
| Anthriscus caucalis | Anthriscus caucalis |
| Antirrhinum vexillocalyculatum | Antirrhinum vexillocalyculatum |
| Antirrhinum vexillocalyculatum ssp. breweri | Antirrhinum vexillocalyculatum ssp. breweri |
| Antirrhinum vexillocalyculatum ssp. vexillocalyculatum | Antirrhinum vexillocalyculatum ssp. vexillocalyculatum |
| Aphanes occidentalis | Aphanes occidentalis |
| Aphyllon californicum | Aphyllon californicum |
| Aphyllon californicum ssp. jepsonii | Aphyllon californicum ssp. jepsonii |
| Aphyllon epigalium | Aphyllon epigalium |
| Aphyllon epigalium ssp. epigalium | Aphyllon epigalium ssp. epigalium |
| Aphyllon fasciculatum | Aphyllon fasciculatum |
| Aphyllon purpureum | Aphyllon purpureum |
| Aphyllon tuberosum | Aphyllon tuberosum |
| Apiastrum angustifolium | Apiastrum angustifolium |
| Apium graveolens | Apium graveolens |
| Apocynum androsaemifolium | Apocynum androsaemifolium |
| Apocynum cannabinum | Apocynum cannabinum |
| Aquilegia formosa | Aquilegia formosa |
| Arabis modesta | Arabis modesta |
| Aralia californica | Aralia californica |
| Arbutus menziesii | Arbutus menziesii |
| Arbutus unedo | Arbutus unedo |
| Arctostaphylos bakeri | Arctostaphylos bakeri |
| Arctostaphylos bakeri ssp. bakeri | Arctostaphylos bakeri ssp. bakeri |
| Arctostaphylos canescens | Arctostaphylos canescens |
| Arctostaphylos glandulosa | Arctostaphylos glandulosa |
| Arctostaphylos glandulosa ssp. cushingiana | Arctostaphylos glandulosa ssp. cushingiana |
| Arctostaphylos glandulosa ssp. glandulosa | Arctostaphylos glandulosa ssp. glandulosa |
| Arctostaphylos glandulosa ssp. mollis | Arctostaphylos glandulosa ssp. mollis |
| Arctostaphylos manzanita | Arctostaphylos manzanita |
| Arctostaphylos manzanita ssp. manzanita | Arctostaphylos manzanita ssp. manzanita |
| Arctostaphylos tomentosa | Arctostaphylos tomentosa |
| Arctostaphylos Xcampbelliae | Arctostaphylos Xcampbelliae |
| Arctotheca calendula | Arctotheca calendula |
| Arctotheca prostrata | Arctotheca prostrata |
| Aristida oligantha | Aristida oligantha |
| Aristolochia californica | Aristolochia californica |
| Arnica discoidea | Arnica discoidea |
| Artemisia californica | Artemisia californica |
| Artemisia douglasiana | Artemisia douglasiana |
| Artemisia dracunculus | Artemisia dracunculus |
| Artemisia ludoviciana | Artemisia ludoviciana |
| Artemisia vulgaris | Artemisia vulgaris |
| Arthrocnemum subterminale | Arthrocnemum subterminale |
| Arum italicum | Arum italicum |
| Arundo donax | Arundo donax |
| Asclepias cordifolia | Asclepias cordifolia |
| Asclepias eriocarpa | Asclepias eriocarpa |
| Asclepias fascicularis | Asclepias fascicularis |
| Asclepias speciosa | Asclepias speciosa |
| Asparagus asparagoides | Asparagus asparagoides |
| Asparagus officinalis | Asparagus officinalis |
| Asparagus officinalis ssp. officinalis | Asparagus officinalis ssp. officinalis |
| Astragalus asymmetricus | Astragalus asymmetricus |
| Astragalus gambelianus | Astragalus gambelianus |
| Astragalus tener | Astragalus tener |
| Astragalus tener var. ferrisiae | Astragalus tener var. ferrisiae |
| Astragalus tener var. tener | Astragalus tener var. tener |
| Athysanus pusillus | Athysanus pusillus |
| Atriplex argentea | Atriplex argentea |
| Atriplex argentea var. expansa | Atriplex argentea var. expansa |
| Atriplex cordulata | Atriplex cordulata |
| Atriplex cordulata var. cordulata | Atriplex cordulata var. cordulata |
| Atriplex coronata | Atriplex coronata |
| Atriplex coronata var. coronata | Atriplex coronata var. coronata |
| Atriplex depressa | Atriplex depressa |
| Atriplex dioica | Atriplex dioica |
| Atriplex fruticulosa | Atriplex fruticulosa |
| Atriplex lentiformis | Atriplex lentiformis |
| Atriplex parishii | Atriplex parishii |
| Atriplex patula | Atriplex patula |
| Atriplex persistens | Atriplex persistens |
| Atriplex prostrata | Atriplex prostrata |
| Atriplex rosea | Atriplex rosea |
| Atriplex semibaccata | Atriplex semibaccata |
| Atriplex serenana | Atriplex serenana |
| Atriplex suberecta | Atriplex suberecta |
| Avena barbata | Avena barbata |
| Avena fatua | Avena fatua |
| Avena sativa | Avena sativa |
| Azolla filiculoides | Azolla filiculoides |
| Baccharis glutinosa | Baccharis glutinosa |
| Baccharis pilularis | Baccharis pilularis |
| Baccharis pilularis ssp. consanguinea | Baccharis pilularis ssp. consanguinea |
| Baccharis salicifolia | Baccharis salicifolia |
| Baccharis salicifolia ssp. salicifolia | Baccharis salicifolia ssp. salicifolia |
| Balsamorhiza deltoidea | Balsamorhiza deltoidea |
| Balsamorhiza macrolepis | Balsamorhiza macrolepis |
| Barbarea orthoceras | Barbarea orthoceras |
| Barbarea verna | Barbarea verna |
| Barbarea vulgaris | Barbarea vulgaris |
| Bassia hyssopifolia | Bassia hyssopifolia |
| Bassia scoparia | Bassia scoparia |
| Bellardia trixago | Bellardia trixago |
| Bellis perennis | Bellis perennis |
| Berberis aquifolium | Berberis aquifolium |
| Berberis aquifolium var. dictyota | Berberis aquifolium var. dictyota |
| Berberis aquifolium var. repens | Berberis aquifolium var. repens |
| Berberis pinnata | Berberis pinnata |
| Berula erecta | Berula erecta |
| Beta vulgaris | Beta vulgaris |
| Beta vulgaris ssp. maritima | Beta vulgaris ssp. maritima |
| Bidens frondosa | Bidens frondosa |
| Bidens laevis | Bidens laevis |
| Bistorta bistortoides | Bistorta bistortoides |
| Blennosperma nanum | Blennosperma nanum |
| Blennosperma nanum var. nanum | Blennosperma nanum var. nanum |
| Blepharizonia plumosa | Blepharizonia plumosa |
| Bolboschoenus fluviatilis | Bolboschoenus fluviatilis |
| Bolboschoenus glaucus | Bolboschoenus glaucus |
| Bolboschoenus maritimus | Bolboschoenus maritimus |
| Bolboschoenus maritimus ssp. paludosus | Bolboschoenus maritimus ssp. paludosus |
| Bolboschoenus robustus | Bolboschoenus robustus |
| Borago officinalis | Borago officinalis |
| Bothriochloa laguroides | Bothriochloa laguroides |
| Bothriochloa laguroides ssp. torreyana | Bothriochloa laguroides ssp. torreyana |
| Bowlesia incana | Bowlesia incana |
| Boykinia occidentalis | Boykinia occidentalis |
| Brachypodium distachyon | Brachypodium distachyon |
| Brassica juncea | Brassica juncea |
| Brassica nigra | Brassica nigra |
| Brassica rapa | Brassica rapa |
| Brassica rapa var. rapa | Brassica rapa var. rapa |
| Brickellia californica | Brickellia californica |
| Briza maxima | Briza maxima |
| Briza minor | Briza minor |
| Brodiaea coronaria | Brodiaea coronaria |
| Brodiaea elegans | Brodiaea elegans |
| Brodiaea elegans ssp. elegans | Brodiaea elegans ssp. elegans |
| Brodiaea leptandra | Brodiaea leptandra |
| Brodiaea terrestris | Brodiaea terrestris |
| Brodiaea terrestris ssp. terrestris | Brodiaea terrestris ssp. terrestris |
| Bromus berteroanus | Bromus berteroanus |
| Bromus caroli-henrici | Bromus caroli-henrici |
| Bromus catharticus | Bromus catharticus |
| Bromus diandrus | Bromus diandrus |
| Bromus hordeaceus | Bromus hordeaceus |
| Bromus japonicus | Bromus japonicus |
| Bromus laevipes | Bromus laevipes |
| Bromus madritensis | Bromus madritensis |
| Bromus madritensis ssp. madritensis | Bromus madritensis ssp. madritensis |
| Bromus racemosus | Bromus racemosus |
| Bromus rubens | Bromus rubens |
| Bromus sitchensis var. carinatus | Bromus sitchensis var. carinatus |
| Bromus sterilis | Bromus sterilis |
| Bromus tectorum | Bromus tectorum |
| Calandrinia breweri | Calandrinia breweri |
| Calandrinia menziesii | Calandrinia menziesii |
| Calendula arvensis | Calendula arvensis |
| Calendula officinalis | Calendula officinalis |
| California macrophylla | California macrophylla |
| Callistemon citrinus | Callistemon citrinus |
| Callitriche fassettii | Callitriche fassettii |
| Callitriche heterophylla | Callitriche heterophylla |
| Callitriche heterophylla var. bolanderi | Callitriche heterophylla var. bolanderi |
| Callitriche longipedunculata | Callitriche longipedunculata |
| Callitriche marginata | Callitriche marginata |
| Calochortus albus | Calochortus albus |
| Calochortus amabilis | Calochortus amabilis |
| Calochortus coeruleus | Calochortus coeruleus |
| Calochortus luteus | Calochortus luteus |
| Calochortus monophyllus | Calochortus monophyllus |
| Calochortus pulchellus | Calochortus pulchellus |
| Calochortus splendens | Calochortus splendens |
| Calochortus superbus | Calochortus superbus |
| Calochortus venustus | Calochortus venustus |
| Calycadenia fremontii | Calycadenia fremontii |
| Calycadenia multiglandulosa | Calycadenia multiglandulosa |
| Calycadenia pauciflora | Calycadenia pauciflora |
| Calycadenia truncata | Calycadenia truncata |
| Calycanthus occidentalis | Calycanthus occidentalis |
| Calystegia collina | Calystegia collina |
| Calystegia macrostegia | Calystegia macrostegia |
| Calystegia macrostegia ssp. cyclostegia | Calystegia macrostegia ssp. cyclostegia |
| Calystegia occidentalis | Calystegia occidentalis |
| Calystegia occidentalis ssp. occidentalis | Calystegia occidentalis ssp. occidentalis |
| Calystegia purpurata | Calystegia purpurata |
| Calystegia purpurata ssp. purpurata | Calystegia purpurata ssp. purpurata |
| Calystegia sepium | Calystegia sepium |
| Calystegia sepium ssp. binghamiae | Calystegia sepium ssp. binghamiae |
| Calystegia sepium ssp. limnophila | Calystegia sepium ssp. limnophila |
| Calystegia subacaulis | Calystegia subacaulis |
| Calystegia subacaulis ssp. subacaulis | Calystegia subacaulis ssp. subacaulis |
| Camissoniopsis cheiranthifolia | Camissoniopsis cheiranthifolia |
| Camissoniopsis cheiranthifolia ssp. cheiranthifolia | Camissoniopsis cheiranthifolia ssp. cheiranthifolia |
| Camissoniopsis hirtella | Camissoniopsis hirtella |
| Camissoniopsis intermedia | Camissoniopsis intermedia |
| Campanula angustiflora | Campanula angustiflora |
| Capsella bursa-pastoris | Capsella bursa-pastoris |
| Cardamine californica | Cardamine californica |
| Cardamine hirsuta | Cardamine hirsuta |
| Cardamine oligosperma | Cardamine oligosperma |
| Cardamine parviflora | Cardamine parviflora |
| Cardamine pensylvanica | Cardamine pensylvanica |
| Carduus pycnocephalus | Carduus pycnocephalus |
| Carduus pycnocephalus ssp. pycnocephalus | Carduus pycnocephalus ssp. pycnocephalus |
| Carduus tenuiflorus | Carduus tenuiflorus |
| Carex barbarae | Carex barbarae |
| Carex bolanderi | Carex bolanderi |
| Carex densa | Carex densa |
| Carex lyngbyei | Carex lyngbyei |
| Carex nudata | Carex nudata |
| Carex praegracilis | Carex praegracilis |
| Carex schottii | Carex schottii |
| Carex senta | Carex senta |
| Carex serratodens | Carex serratodens |
| Carex tumulicola | Carex tumulicola |
| Carpobrotus chilensis | Carpobrotus chilensis |
| Carpobrotus edulis | Carpobrotus edulis |
| Carthamus creticus | Carthamus creticus |
| Carthamus lanatus | Carthamus lanatus |
| Carthamus tinctorius | Carthamus tinctorius |
| Carya illinoinensis | Carya illinoinensis |
| Castilleja affinis | Castilleja affinis |
| Castilleja affinis ssp. affinis | Castilleja affinis ssp. affinis |
| Castilleja affinis ssp. neglecta | Castilleja affinis ssp. neglecta |
| Castilleja affinis var. neglecta | Castilleja affinis var. neglecta |
| Castilleja ambigua | Castilleja ambigua |
| Castilleja ambigua ssp. ambigua | Castilleja ambigua ssp. ambigua |
| Castilleja ambigua var. ambigua | Castilleja ambigua var. ambigua |
| Castilleja applegatei | Castilleja applegatei |
| Castilleja applegatei ssp. martinii | Castilleja applegatei ssp. martinii |
| Castilleja attenuata | Castilleja attenuata |
| Castilleja campestris | Castilleja campestris |
| Castilleja campestris ssp. campestris | Castilleja campestris ssp. campestris |
| Castilleja campestris ssp. succulenta | Castilleja campestris ssp. succulenta |
| Castilleja campestris var. succulenta | Castilleja campestris var. succulenta |
| Castilleja densiflora | Castilleja densiflora |
| Castilleja densiflora ssp. densiflora | Castilleja densiflora ssp. densiflora |
| Castilleja exserta | Castilleja exserta |
| Castilleja exserta ssp. exserta | Castilleja exserta ssp. exserta |
| Castilleja foliolosa | Castilleja foliolosa |
| Castilleja rubicundula | Castilleja rubicundula |
| Castilleja rubicundula ssp. lithospermoides | Castilleja rubicundula ssp. lithospermoides |
| Castilleja subinclusa | Castilleja subinclusa |
| Caulanthus flavescens | Caulanthus flavescens |
| Caulanthus lasiophyllus | Caulanthus lasiophyllus |
| Ceanothus cordulatus | Ceanothus cordulatus |
| Ceanothus cuneatus | Ceanothus cuneatus |
| Ceanothus cuneatus var. cuneatus | Ceanothus cuneatus var. cuneatus |
| Ceanothus integerrimus | Ceanothus integerrimus |
| Ceanothus maritimus | Ceanothus maritimus |
| Ceanothus oliganthus | Ceanothus oliganthus |
| Ceanothus oliganthus var. sorediatus | Ceanothus oliganthus var. sorediatus |
| Ceanothus parryi | Ceanothus parryi |
| Ceanothus purpureus | Ceanothus purpureus |
| Ceanothus thyrsiflorus | Ceanothus thyrsiflorus |
| Ceanothus tomentosus | Ceanothus tomentosus |
| Celtis laevigata | Celtis laevigata |
| Cenchrus echinatus | Cenchrus echinatus |
| Cenchrus incertus | Cenchrus incertus |
| Cenchrus longispinus | Cenchrus longispinus |
| Cenchrus spinifex | Cenchrus spinifex |
| Centaurea calcitrapa | Centaurea calcitrapa |
| Centaurea cyanus | Centaurea cyanus |
| Centaurea diffusa | Centaurea diffusa |
| Centaurea iberica | Centaurea iberica |
| Centaurea melitensis | Centaurea melitensis |
| Centaurea solstitialis | Centaurea solstitialis |
| Centaurium tenuiflorum | Centaurium tenuiflorum |
| Centranthus ruber | Centranthus ruber |
| Centromadia fitchii | Centromadia fitchii |
| Centromadia parryi | Centromadia parryi |
| Centromadia parryi ssp. congdonii | Centromadia parryi ssp. congdonii |
| Centromadia parryi ssp. parryi | Centromadia parryi ssp. parryi |
| Centromadia parryi ssp. rudis | Centromadia parryi ssp. rudis |
| Centromadia pungens | Centromadia pungens |
| Centromadia pungens ssp. pungens | Centromadia pungens ssp. pungens |
| Cephalanthus occidentalis | Cephalanthus occidentalis |
| Cerastium arvense | Cerastium arvense |
| Cerastium arvense ssp. strictum | Cerastium arvense ssp. strictum |
| Cerastium fontanum | Cerastium fontanum |
| Cerastium fontanum ssp. vulgare | Cerastium fontanum ssp. vulgare |
| Cerastium glomeratum | Cerastium glomeratum |
| Ceratophyllum demersum | Ceratophyllum demersum |
| Cercis occidentalis | Cercis occidentalis |
| Cercocarpus betuloides | Cercocarpus betuloides |
| Cercocarpus betuloides var. betuloides | Cercocarpus betuloides var. betuloides |
| Chaenactis glabriuscula | Chaenactis glabriuscula |
| Chaenactis glabriuscula var. heterocarpha | Chaenactis glabriuscula var. heterocarpha |
| Chenopodium album | Chenopodium album |
| Chenopodium berlandieri | Chenopodium berlandieri |
| Chenopodium californicum | Chenopodium californicum |
| Chenopodium carnosulum | Chenopodium carnosulum |
| Chenopodium macrospermum | Chenopodium macrospermum |
| Chenopodium murale | Chenopodium murale |
| Chenopodium rubrum | Chenopodium rubrum |
| Chenopodium rubrum var. rubrum | Chenopodium rubrum var. rubrum |
| Chenopodium vulvaria | Chenopodium vulvaria |
| Chlorogalum angustifolium | Chlorogalum angustifolium |
| Chlorogalum pomeridianum | Chlorogalum pomeridianum |
| Chlorogalum pomeridianum var. pomeridianum | Chlorogalum pomeridianum var. pomeridianum |
| Chloropyron molle | Chloropyron molle |
| Chloropyron molle ssp. hispidum | Chloropyron molle ssp. hispidum |
| Chloropyron molle ssp. molle | Chloropyron molle ssp. molle |
| Chondrilla juncea | Chondrilla juncea |
| Chorizanthe membranacea | Chorizanthe membranacea |
| Chorizanthe polygonoides | Chorizanthe polygonoides |
| Chorizanthe polygonoides var. polygonoides | Chorizanthe polygonoides var. polygonoides |
| Cicendia quadrangularis | Cicendia quadrangularis |
| Cichorium intybus | Cichorium intybus |
| Cicuta douglasii | Cicuta douglasii |
| Cicuta maculata | Cicuta maculata |
| Cicuta maculata var. bolanderi | Cicuta maculata var. bolanderi |
| Cirsium arvense | Cirsium arvense |
| Cirsium cymosum | Cirsium cymosum |
| Cirsium hydrophilum | Cirsium hydrophilum |
| Cirsium hydrophilum var. hydrophilum | Cirsium hydrophilum var. hydrophilum |
| Cirsium occidentale | Cirsium occidentale |
| Cirsium occidentale var. venustum | Cirsium occidentale var. venustum |
| Cirsium quercetorum | Cirsium quercetorum |
| Cirsium vulgare | Cirsium vulgare |
| Clarkia affinis | Clarkia affinis |
| Clarkia concinna | Clarkia concinna |
| Clarkia concinna ssp. concinna | Clarkia concinna ssp. concinna |
| Clarkia gracilis | Clarkia gracilis |
| Clarkia gracilis ssp. albicaulis | Clarkia gracilis ssp. albicaulis |
| Clarkia gracilis ssp. gracilis | Clarkia gracilis ssp. gracilis |
| Clarkia purpurea | Clarkia purpurea |
| Clarkia purpurea ssp. purpurea | Clarkia purpurea ssp. purpurea |
| Clarkia purpurea ssp. quadrivulnera | Clarkia purpurea ssp. quadrivulnera |
| Clarkia unguiculata | Clarkia unguiculata |
| Claytonia exigua ssp. glauca | Claytonia exigua ssp. glauca |
| Claytonia parviflora | Claytonia parviflora |
| Claytonia parviflora ssp. parviflora | Claytonia parviflora ssp. parviflora |
| Claytonia parviflora ssp. utahensis | Claytonia parviflora ssp. utahensis |
| Claytonia perfoliata | Claytonia perfoliata |
| Claytonia perfoliata ssp. mexicana | Claytonia perfoliata ssp. mexicana |
| Claytonia perfoliata ssp. perfoliata | Claytonia perfoliata ssp. perfoliata |
| Clematis lasiantha | Clematis lasiantha |
| Clematis ligusticifolia | Clematis ligusticifolia |
| Clinopodium mimuloides | Clinopodium mimuloides |
| Collinsia bartsiifolia | Collinsia bartsiifolia |
| Collinsia bartsiifolia var. bartsiifolia | Collinsia bartsiifolia var. bartsiifolia |
| Collinsia heterophylla | Collinsia heterophylla |
| Collinsia heterophylla var. heterophylla | Collinsia heterophylla var. heterophylla |
| Collinsia sparsiflora | Collinsia sparsiflora |
| Collinsia sparsiflora var. arvensis | Collinsia sparsiflora var. arvensis |
| Collinsia sparsiflora var. collina | Collinsia sparsiflora var. collina |
| Collinsia sparsiflora var. sparsiflora | Collinsia sparsiflora var. sparsiflora |
| Collomia heterophylla | Collomia heterophylla |
| Colocasia esculenta | Colocasia esculenta |
| Conium maculatum | Conium maculatum |
| Convolvulus arvensis | Convolvulus arvensis |
| Convolvulus simulans | Convolvulus simulans |
| Cordylanthus pilosus | Cordylanthus pilosus |
| Cordylanthus pilosus ssp. pilosus | Cordylanthus pilosus ssp. pilosus |
| Coriandrum sativum | Coriandrum sativum |
| Cornus glabrata | Cornus glabrata |
| Cornus sericea | Cornus sericea |
| Cornus sericea ssp. occidentalis | Cornus sericea ssp. occidentalis |
| Cornus sericea ssp. sericea | Cornus sericea ssp. sericea |
| Cortaderia jubata | Cortaderia jubata |
| Cortaderia selloana | Cortaderia selloana |
| Corylus cornuta | Corylus cornuta |
| Corylus cornuta ssp. californica | Corylus cornuta ssp. californica |
| Cotoneaster lacteus | Cotoneaster lacteus |
| Cotoneaster pannosus | Cotoneaster pannosus |
| Cotula australis | Cotula australis |
| Cotula coronopifolia | Cotula coronopifolia |
| Crassula aquatica | Crassula aquatica |
| Crassula connata | Crassula connata |
| Crassula solieri | Crassula solieri |
| Crassula tillaea | Crassula tillaea |
| Crataegus gaylussacia | Crataegus gaylussacia |
| Crataegus monogyna | Crataegus monogyna |
| Crepis pulchra | Crepis pulchra |
| Cressa truxillensis | Cressa truxillensis |
| Crocanthemum scoparium | Crocanthemum scoparium |
| Crocanthemum scoparium var. vulgare | Crocanthemum scoparium var. vulgare |
| Croton setiger | Croton setiger |
| Crypsis schoenoides | Crypsis schoenoides |
| Crypsis vaginiflora | Crypsis vaginiflora |
| Cryptantha flaccida | Cryptantha flaccida |
| Cryptantha hooveri | Cryptantha hooveri |
| Cryptantha intermedia | Cryptantha intermedia |
| Cryptantha muricata | Cryptantha muricata |
| Cuscuta californica | Cuscuta californica |
| Cuscuta campestris | Cuscuta campestris |
| Cuscuta howelliana | Cuscuta howelliana |
| Cuscuta indecora | Cuscuta indecora |
| Cuscuta indecora var. indecora | Cuscuta indecora var. indecora |
| Cuscuta jepsonii | Cuscuta jepsonii |
| Cuscuta pacifica | Cuscuta pacifica |
| Cuscuta pacifica var. pacifica | Cuscuta pacifica var. pacifica |
| Cuscuta pacifica var. papillata | Cuscuta pacifica var. papillata |
| Cuscuta pentagona | Cuscuta pentagona |
| Cuscuta salina | Cuscuta salina |
| Cuscuta subinclusa | Cuscuta subinclusa |
| Cynara cardunculus | Cynara cardunculus |
| Cynara cardunculus ssp. cardunculus | Cynara cardunculus ssp. cardunculus |
| Cynodon dactylon | Cynodon dactylon |
| Cynosurus echinatus | Cynosurus echinatus |
| Cyperus acuminatus | Cyperus acuminatus |
| Cyperus eragrostis | Cyperus eragrostis |
| Cyperus esculentus | Cyperus esculentus |
| Cyperus esculentus var. leptostachyus | Cyperus esculentus var. leptostachyus |
| Cyperus involucratus | Cyperus involucratus |
| Cyperus niger | Cyperus niger |
| Cyperus odoratus | Cyperus odoratus |
| Cystopteris fragilis | Cystopteris fragilis |
| Cytisus scoparius | Cytisus scoparius |
| Dactylis glomerata | Dactylis glomerata |
| Damasonium californicum | Damasonium californicum |
| Danthonia californica | Danthonia californica |
| Datisca glomerata | Datisca glomerata |
| Datura inoxia | Datura inoxia |
| Datura stramonium | Datura stramonium |
| Datura wrightii | Datura wrightii |
| Daucus carota | Daucus carota |
| Daucus pusillus | Daucus pusillus |
| Deinandra lobbii | Deinandra lobbii |
| Delairea odorata | Delairea odorata |
| Delphinium decorum | Delphinium decorum |
| Delphinium hansenii | Delphinium hansenii |
| Delphinium hesperium | Delphinium hesperium |
| Delphinium hesperium ssp. hesperium | Delphinium hesperium ssp. hesperium |
| Delphinium hesperium ssp. pallescens | Delphinium hesperium ssp. pallescens |
| Delphinium nudicaule | Delphinium nudicaule |
| Delphinium patens | Delphinium patens |
| Delphinium patens ssp. patens | Delphinium patens ssp. patens |
| Delphinium recurvatum | Delphinium recurvatum |
| Delphinium variegatum | Delphinium variegatum |
| Delphinium variegatum ssp. variegatum | Delphinium variegatum ssp. variegatum |
| Dendromecon rigida | Dendromecon rigida |
| Deschampsia cespitosa | Deschampsia cespitosa |
| Deschampsia cespitosa ssp. cespitosa | Deschampsia cespitosa ssp. cespitosa |
| Deschampsia cespitosa ssp. holciformis | Deschampsia cespitosa ssp. holciformis |
| Deschampsia danthonioides | Deschampsia danthonioides |
| Deschampsia elongata | Deschampsia elongata |
| Descurainia sophia | Descurainia sophia |
| Dichelostemma congestum | Dichelostemma congestum |
| Dichelostemma multiflorum | Dichelostemma multiflorum |
| Dichelostemma volubile | Dichelostemma volubile |
| Dichondra micrantha | Dichondra micrantha |
| Digitalis purpurea | Digitalis purpurea |
| Digitaria sanguinalis | Digitaria sanguinalis |
| Diospyros lotus | Diospyros lotus |
| Diplacus aurantiacus | Diplacus aurantiacus |
| Diplacus douglasii | Diplacus douglasii |
| Diplacus tricolor | Diplacus tricolor |
| Dipsacus fullonum | Dipsacus fullonum |
| Dipsacus sativus | Dipsacus sativus |
| Dipterostemon capitatus | Dipterostemon capitatus |
| Dipterostemon capitatus ssp. capitatus | Dipterostemon capitatus ssp. capitatus |
| Dirca occidentalis | Dirca occidentalis |
| Distichlis spicata | Distichlis spicata |
| Dittrichia graveolens | Dittrichia graveolens |
| Dittrichia viscosa | Dittrichia viscosa |
| Downingia bella | Downingia bella |
| Downingia bicornuta | Downingia bicornuta |
| Downingia bicornuta var. bicornuta | Downingia bicornuta var. bicornuta |
| Downingia concolor | Downingia concolor |
| Downingia concolor var. concolor | Downingia concolor var. concolor |
| Downingia cuspidata | Downingia cuspidata |
| Downingia insignis | Downingia insignis |
| Downingia ornatissima | Downingia ornatissima |
| Downingia ornatissima var. mirabilis | Downingia ornatissima var. mirabilis |
| Downingia ornatissima var. ornatissima | Downingia ornatissima var. ornatissima |
| Downingia pulchella | Downingia pulchella |
| Downingia pusilla | Downingia pusilla |
| Draba verna | Draba verna |
| Drymocallis glandulosa | Drymocallis glandulosa |
| Drymocallis glandulosa var. wrangelliana | Drymocallis glandulosa var. wrangelliana |
| Dryopteris arguta | Dryopteris arguta |
| Duchesnea indica | Duchesnea indica |
| Duchesnea indica var. indica | Duchesnea indica var. indica |
| Dudleya caespitosa | Dudleya caespitosa |
| Dudleya cymosa | Dudleya cymosa |
| Dudleya farinosa | Dudleya farinosa |
| Dysphania ambrosioides | Dysphania ambrosioides |
| Dysphania chilensis | Dysphania chilensis |
| Dysphania multifida | Dysphania multifida |
| Echinochloa colona | Echinochloa colona |
| Echinochloa crus-galli | Echinochloa crus-galli |
| Echinochloa crus-pavonis | Echinochloa crus-pavonis |
| Echinochloa crus-pavonis var. crus-pavonis | Echinochloa crus-pavonis var. crus-pavonis |
| Echinochloa muricata | Echinochloa muricata |
| Echinochloa oryzoides | Echinochloa oryzoides |
| Echium candicans | Echium candicans |
| Eclipta prostrata | Eclipta prostrata |
| Egeria densa | Egeria densa |
| Ehrendorferia chrysantha | Ehrendorferia chrysantha |
| Eichhornia crassipes | Eichhornia crassipes |
| Elaeagnus angustifolia | Elaeagnus angustifolia |
| Elatine ambigua | Elatine ambigua |
| Elatine californica | Elatine californica |
| Elatine rubella | Elatine rubella |
| Eleocharis acicularis | Eleocharis acicularis |
| Eleocharis acicularis var. acicularis | Eleocharis acicularis var. acicularis |
| Eleocharis macrostachya | Eleocharis macrostachya |
| Eleocharis parvula | Eleocharis parvula |
| Elodea canadensis | Elodea canadensis |
| Elymus caput-medusae | Elymus caput-medusae |
| Elymus elymoides | Elymus elymoides |
| Elymus glaucus | Elymus glaucus |
| Elymus glaucus ssp. glaucus | Elymus glaucus ssp. glaucus |
| Elymus multisetus | Elymus multisetus |
| Elymus ponticus | Elymus ponticus |
| Elymus repens | Elymus repens |
| Elymus trachycaulus | Elymus trachycaulus |
| Elymus trachycaulus ssp. trachycaulus | Elymus trachycaulus ssp. trachycaulus |
| Elymus triticoides | Elymus triticoides |
| Elymus Xhansenii | Elymus Xhansenii |
| Emmenanthe penduliflora | Emmenanthe penduliflora |
| Emmenanthe penduliflora var. penduliflora | Emmenanthe penduliflora var. penduliflora |
| Enemion occidentale | Enemion occidentale |
| Epilobium brachycarpum | Epilobium brachycarpum |
| Epilobium campestre | Epilobium campestre |
| Epilobium canum | Epilobium canum |
| Epilobium canum ssp. canum | Epilobium canum ssp. canum |
| Epilobium canum ssp. latifolium | Epilobium canum ssp. latifolium |
| Epilobium ciliatum | Epilobium ciliatum |
| Epilobium ciliatum ssp. ciliatum | Epilobium ciliatum ssp. ciliatum |
| Epilobium ciliatum ssp. watsonii | Epilobium ciliatum ssp. watsonii |
| Epilobium cleistogamum | Epilobium cleistogamum |
| Epilobium densiflorum | Epilobium densiflorum |
| Epilobium minutum | Epilobium minutum |
| Epilobium pallidum | Epilobium pallidum |
| Epilobium torreyi | Epilobium torreyi |
| Epipactis gigantea | Epipactis gigantea |
| Equisetum arvense | Equisetum arvense |
| Equisetum hyemale | Equisetum hyemale |
| Equisetum hyemale ssp. affine | Equisetum hyemale ssp. affine |
| Equisetum laevigatum | Equisetum laevigatum |
| Equisetum telmateia | Equisetum telmateia |
| Equisetum telmateia ssp. braunii | Equisetum telmateia ssp. braunii |
| Equisetum Xferrissii | Equisetum Xferrissii |
| Eragrostis barrelieri | Eragrostis barrelieri |
| Eragrostis cilianensis | Eragrostis cilianensis |
| Eragrostis curvula | Eragrostis curvula |
| Eragrostis hypnoides | Eragrostis hypnoides |
| Eragrostis minor | Eragrostis minor |
| Eragrostis pectinacea | Eragrostis pectinacea |
| Eragrostis pectinacea var. miserrima | Eragrostis pectinacea var. miserrima |
| Eragrostis pectinacea var. pectinacea | Eragrostis pectinacea var. pectinacea |
| Eragrostis pilosa | Eragrostis pilosa |
| Ericameria arborescens | Ericameria arborescens |
| Erigeron biolettii | Erigeron biolettii |
| Erigeron bonariensis | Erigeron bonariensis |
| Erigeron canadensis | Erigeron canadensis |
| Erigeron foliosus | Erigeron foliosus |
| Erigeron foliosus var. franciscensis | Erigeron foliosus var. franciscensis |
| Erigeron foliosus var. hartwegii | Erigeron foliosus var. hartwegii |
| Erigeron greenei | Erigeron greenei |
| Erigeron inornatus | Erigeron inornatus |
| Erigeron petrophilus | Erigeron petrophilus |
| Erigeron philadelphicus | Erigeron philadelphicus |
| Erigeron philadelphicus var. philadelphicus | Erigeron philadelphicus var. philadelphicus |
| Erigeron sumatrensis | Erigeron sumatrensis |
| Eriochloa contracta | Eriochloa contracta |
| Eriodictyon californicum | Eriodictyon californicum |
| Eriogonum angulosum | Eriogonum angulosum |
| Eriogonum dasyanthemum | Eriogonum dasyanthemum |
| Eriogonum fasciculatum | Eriogonum fasciculatum |
| Eriogonum gracile | Eriogonum gracile |
| Eriogonum gracile var. gracile | Eriogonum gracile var. gracile |
| Eriogonum luteolum | Eriogonum luteolum |
| Eriogonum luteolum var. caninum | Eriogonum luteolum var. caninum |
| Eriogonum luteolum var. luteolum | Eriogonum luteolum var. luteolum |
| Eriogonum nudum | Eriogonum nudum |
| Eriogonum nudum var. auriculatum | Eriogonum nudum var. auriculatum |
| Eriogonum nudum var. nudum | Eriogonum nudum var. nudum |
| Eriogonum nudum var. oblongifolium | Eriogonum nudum var. oblongifolium |
| Eriogonum nudum var. psychicola | Eriogonum nudum var. psychicola |
| Eriogonum roseum | Eriogonum roseum |
| Eriogonum truncatum | Eriogonum truncatum |
| Eriophyllum confertiflorum | Eriophyllum confertiflorum |
| Eriophyllum lanatum | Eriophyllum lanatum |
| Eriophyllum lanatum var. achilleoides | Eriophyllum lanatum var. achilleoides |
| Eriophyllum lanatum var. grandiflorum | Eriophyllum lanatum var. grandiflorum |
| Erodium botrys | Erodium botrys |
| Erodium brachycarpum | Erodium brachycarpum |
| Erodium cicutarium | Erodium cicutarium |
| Erodium moschatum | Erodium moschatum |
| Eryngium aristulatum | Eryngium aristulatum |
| Eryngium aristulatum var. aristulatum | Eryngium aristulatum var. aristulatum |
| Eryngium armatum | Eryngium armatum |
| Eryngium articulatum | Eryngium articulatum |
| Eryngium castrense | Eryngium castrense |
| Eryngium jepsonii | Eryngium jepsonii |
| Eryngium vaseyi | Eryngium vaseyi |
| Erysimum capitatum | Erysimum capitatum |
| Erysimum capitatum var. angustatum | Erysimum capitatum var. angustatum |
| Erysimum capitatum var. capitatum | Erysimum capitatum var. capitatum |
| Erysimum menziesii | Erysimum menziesii |
| Erythranthe arvensis | Erythranthe arvensis |
| Erythranthe cardinalis | Erythranthe cardinalis |
| Erythranthe floribunda | Erythranthe floribunda |
| Erythranthe guttata | Erythranthe guttata |
| Erythranthe latidens | Erythranthe latidens |
| Erythranthe microphylla | Erythranthe microphylla |
| Erythranthe nasuta | Erythranthe nasuta |
| Eschscholzia caespitosa | Eschscholzia caespitosa |
| Eschscholzia californica | Eschscholzia californica |
| Eschscholzia lobbii | Eschscholzia lobbii |
| Eschscholzia rhombipetala | Eschscholzia rhombipetala |
| Eucalyptus camaldulensis | Eucalyptus camaldulensis |
| Eucalyptus globulus | Eucalyptus globulus |
| Eucalyptus polyanthemos | Eucalyptus polyanthemos |
| Eucalyptus sideroxylon | Eucalyptus sideroxylon |
| Eucalyptus tereticornis | Eucalyptus tereticornis |
| Eucrypta chrysanthemifolia | Eucrypta chrysanthemifolia |
| Eucrypta chrysanthemifolia var. chrysanthemifolia | Eucrypta chrysanthemifolia var. chrysanthemifolia |
| Euphorbia crenulata | Euphorbia crenulata |
| Euphorbia maculata | Euphorbia maculata |
| Euphorbia oblongata | Euphorbia oblongata |
| Euphorbia ocellata | Euphorbia ocellata |
| Euphorbia peplus | Euphorbia peplus |
| Euphorbia prostrata | Euphorbia prostrata |
| Euphorbia serpens | Euphorbia serpens |
| Euphorbia serpillifolia | Euphorbia serpillifolia |
| Euphorbia serpillifolia ssp. serpillifolia | Euphorbia serpillifolia ssp. serpillifolia |
| Euphorbia spathulata | Euphorbia spathulata |
| Eurybia radulina | Eurybia radulina |
| Euthamia occidentalis | Euthamia occidentalis |
| Extriplex joaquinana | Extriplex joaquinana |
| Fallopia baldschuanica | Fallopia baldschuanica |
| Festuca arundinacea | Festuca arundinacea |
| Festuca bromoides | Festuca bromoides |
| Festuca californica | Festuca californica |
| Festuca elmeri | Festuca elmeri |
| Festuca idahoensis | Festuca idahoensis |
| Festuca microstachys | Festuca microstachys |
| Festuca myuros | Festuca myuros |
| Festuca octoflora | Festuca octoflora |
| Festuca perennis | Festuca perennis |
| Festuca pratensis | Festuca pratensis |
| Festuca rubra | Festuca rubra |
| Festuca temulenta | Festuca temulenta |
| Ficus carica | Ficus carica |
| Foeniculum vulgare | Foeniculum vulgare |
| Fragaria vesca | Fragaria vesca |
| Frangula californica | Frangula californica |
| Frangula californica ssp. californica | Frangula californica ssp. californica |
| Frangula californica ssp. tomentella | Frangula californica ssp. tomentella |
| Frangula rubra | Frangula rubra |
| Frangula rubra ssp. rubra | Frangula rubra ssp. rubra |
| Frankenia salina | Frankenia salina |
| Fraxinus dipetala | Fraxinus dipetala |
| Fraxinus latifolia | Fraxinus latifolia |
| Fraxinus velutina | Fraxinus velutina |
| Fremontodendron californicum | Fremontodendron californicum |
| Fritillaria affinis | Fritillaria affinis |
| Fritillaria agrestis | Fritillaria agrestis |
| Fritillaria liliacea | Fritillaria liliacea |
| Fritillaria pluriflora | Fritillaria pluriflora |
| Fritillaria recurva | Fritillaria recurva |
| Fumaria capreolata | Fumaria capreolata |
| Galium aparine | Galium aparine |
| Galium bolanderi | Galium bolanderi |
| Galium murale | Galium murale |
| Galium nuttallii | Galium nuttallii |
| Galium parisiense | Galium parisiense |
| Galium porrigens | Galium porrigens |
| Galium porrigens var. tenue | Galium porrigens var. tenue |
| Galium tricornutum | Galium tricornutum |
| Galium trifidum | Galium trifidum |
| Galium trifidum ssp. columbianum | Galium trifidum ssp. columbianum |
| Gamochaeta coarctata | Gamochaeta coarctata |
| Gamochaeta ustulata | Gamochaeta ustulata |
| Garrya flavescens | Garrya flavescens |
| Garrya fremontii | Garrya fremontii |
| Gastridium phleoides | Gastridium phleoides |
| Gazania linearis | Gazania linearis |
| Genista monspessulana | Genista monspessulana |
| Geranium dissectum | Geranium dissectum |
| Geranium molle | Geranium molle |
| Geranium purpureum | Geranium purpureum |
| Geranium pusillum | Geranium pusillum |
| Geranium robertianum | Geranium robertianum |
| Gilia achilleifolia | Gilia achilleifolia |
| Gilia achilleifolia ssp. multicaulis | Gilia achilleifolia ssp. multicaulis |
| Gilia capitata | Gilia capitata |
| Gilia capitata ssp. capitata | Gilia capitata ssp. capitata |
| Gilia capitata ssp. staminea | Gilia capitata ssp. staminea |
| Gilia capitata ssp. tomentosa | Gilia capitata ssp. tomentosa |
| Gilia clivorum | Gilia clivorum |
| Gilia tricolor | Gilia tricolor |
| Gilia tricolor ssp. tricolor | Gilia tricolor ssp. tricolor |
| Githopsis diffusa | Githopsis diffusa |
| Githopsis diffusa ssp. robusta | Githopsis diffusa ssp. robusta |
| Githopsis specularioides | Githopsis specularioides |
| Glandularia peruviana | Glandularia peruviana |
| Gleditsia triacanthos | Gleditsia triacanthos |
| Glinus lotoides | Glinus lotoides |
| Glyceria declinata | Glyceria declinata |
| Glyceria Xoccidentalis | Glyceria Xoccidentalis |
| Glycyrrhiza glabra | Glycyrrhiza glabra |
| Glycyrrhiza lepidota | Glycyrrhiza lepidota |
| Gnaphalium palustre | Gnaphalium palustre |
| Gratiola heterosepala | Gratiola heterosepala |
| Grindelia camporum | Grindelia camporum |
| Grindelia hirsutula | Grindelia hirsutula |
| Grindelia stricta | Grindelia stricta |
| Grindelia stricta var. angustifolia | Grindelia stricta var. angustifolia |
| Grindelia stricta var. platyphylla | Grindelia stricta var. platyphylla |
| Grindelia Xpaludosa | Grindelia Xpaludosa |
| Gruvelia pusilla | Gruvelia pusilla |
| Gutierrezia californica | Gutierrezia californica |
| Hainardia cylindrica | Hainardia cylindrica |
| Halimodendron halodendron | Halimodendron halodendron |
| Harmonia nutans | Harmonia nutans |
| Hedera helix | Hedera helix |
| Helenium bigelovii | Helenium bigelovii |
| Helenium puberulum | Helenium puberulum |
| Helianthella californica | Helianthella californica |
| Helianthella californica var. californica | Helianthella californica var. californica |
| Helianthella castanea | Helianthella castanea |
| Helianthus annuus | Helianthus annuus |
| Helianthus bolanderi | Helianthus bolanderi |
| Helianthus californicus | Helianthus californicus |
| Helianthus petiolaris | Helianthus petiolaris |
| Helichrysum petiolare | Helichrysum petiolare |
| Heliotropium amplexicaule | Heliotropium amplexicaule |
| Heliotropium curassavicum | Heliotropium curassavicum |
| Heliotropium curassavicum var. oculatum | Heliotropium curassavicum var. oculatum |
| Heliotropium europaeum | Heliotropium europaeum |
| Helminthotheca echioides | Helminthotheca echioides |
| Hemizonella minima | Hemizonella minima |
| Hemizonia congesta | Hemizonia congesta |
| Hemizonia congesta ssp. congesta | Hemizonia congesta ssp. congesta |
| Hemizonia congesta ssp. lutescens | Hemizonia congesta ssp. lutescens |
| Hemizonia congesta ssp. luzulifolia | Hemizonia congesta ssp. luzulifolia |
| Heracleum maximum | Heracleum maximum |
| Herniaria hirsuta | Herniaria hirsuta |
| Hesperevax acaulis | Hesperevax acaulis |
| Hesperevax caulescens | Hesperevax caulescens |
| Hesperevax sparsiflora | Hesperevax sparsiflora |
| Hesperevax sparsiflora var. sparsiflora | Hesperevax sparsiflora var. sparsiflora |
| Hesperocyparis macrocarpa | Hesperocyparis macrocarpa |
| Hesperocyparis stephensonii | Hesperocyparis stephensonii |
| Hesperolinon breweri | Hesperolinon breweri |
| Hesperolinon californicum | Hesperolinon californicum |
| Hesperolinon clevelandii | Hesperolinon clevelandii |
| Hesperolinon disjunctum | Hesperolinon disjunctum |
| Hesperolinon micranthum | Hesperolinon micranthum |
| Heterocodon rariflorum | Heterocodon rariflorum |
| Heteromeles arbutifolia | Heteromeles arbutifolia |
| Heterotheca grandiflora | Heterotheca grandiflora |
| Heterotheca sessiliflora | Heterotheca sessiliflora |
| Heterotheca sessiliflora ssp. bolanderi | Heterotheca sessiliflora ssp. bolanderi |
| Heterotheca sessiliflora ssp. echioides | Heterotheca sessiliflora ssp. echioides |
| Hibiscus lasiocarpos | Hibiscus lasiocarpos |
| Hibiscus lasiocarpos var. occidentalis | Hibiscus lasiocarpos var. occidentalis |
| Hibiscus trionum | Hibiscus trionum |
| Hieracium albiflorum | Hieracium albiflorum |
| Hirschfeldia incana | Hirschfeldia incana |
| Hoita macrostachya | Hoita macrostachya |
| Holcus lanatus | Holcus lanatus |
| Holocarpha heermannii | Holocarpha heermannii |
| Holocarpha macradenia | Holocarpha macradenia |
| Holocarpha virgata | Holocarpha virgata |
| Holocarpha virgata ssp. virgata | Holocarpha virgata ssp. virgata |
| Holodiscus discolor | Holodiscus discolor |
| Holosteum umbellatum | Holosteum umbellatum |
| Hordeum arizonicum | Hordeum arizonicum |
| Hordeum brachyantherum | Hordeum brachyantherum |
| Hordeum brachyantherum ssp. brachyantherum | Hordeum brachyantherum ssp. brachyantherum |
| Hordeum brachyantherum ssp. californicum | Hordeum brachyantherum ssp. californicum |
| Hordeum depressum | Hordeum depressum |
| Hordeum jubatum | Hordeum jubatum |
| Hordeum marinum | Hordeum marinum |
| Hordeum marinum ssp. gussoneanum | Hordeum marinum ssp. gussoneanum |
| Hordeum murinum | Hordeum murinum |
| Hordeum murinum ssp. glaucum | Hordeum murinum ssp. glaucum |
| Hordeum murinum ssp. leporinum | Hordeum murinum ssp. leporinum |
| Hordeum vulgare | Hordeum vulgare |
| Hornungia procumbens | Hornungia procumbens |
| Hosackia crassifolia | Hosackia crassifolia |
| Hosackia crassifolia var. crassifolia | Hosackia crassifolia var. crassifolia |
| Hydrocotyle ranunculoides | Hydrocotyle ranunculoides |
| Hydrocotyle verticillata | Hydrocotyle verticillata |
| Hypericum concinnum | Hypericum concinnum |
| Hypericum perforatum | Hypericum perforatum |
| Hypericum perforatum ssp. perforatum | Hypericum perforatum ssp. perforatum |
| Hypochaeris glabra | Hypochaeris glabra |
| Hypochaeris radicata | Hypochaeris radicata |
| Ipomoea indica | Ipomoea indica |
| Ipomoea purpurea | Ipomoea purpurea |
| Iris douglasiana | Iris douglasiana |
| Iris fernaldii | Iris fernaldii |
| Iris foetidissima | Iris foetidissima |
| Iris longipetala | Iris longipetala |
| Iris macrosiphon | Iris macrosiphon |
| Iris missouriensis | Iris missouriensis |
| Iris pseudacorus | Iris pseudacorus |
| Isocoma arguta | Isocoma arguta |
| Isocoma menziesii | Isocoma menziesii |
| Isocoma menziesii var. vernonioides | Isocoma menziesii var. vernonioides |
| Isoetes howellii | Isoetes howellii |
| Isoetes nuttallii | Isoetes nuttallii |
| Isoetes orcuttii | Isoetes orcuttii |
| Isolepis carinata | Isolepis carinata |
| Isolepis cernua | Isolepis cernua |
| Iva axillaris | Iva axillaris |
| Jaumea carnosa | Jaumea carnosa |
| Juglans californica | Juglans californica |
| Juglans hindsii | Juglans hindsii |
| Juglans regia | Juglans regia |
| Juncus acutus | Juncus acutus |
| Juncus acutus ssp. leopoldii | Juncus acutus ssp. leopoldii |
| Juncus ambiguus | Juncus ambiguus |
| Juncus balticus | Juncus balticus |
| Juncus balticus ssp. ater | Juncus balticus ssp. ater |
| Juncus bolanderi | Juncus bolanderi |
| Juncus breweri | Juncus breweri |
| Juncus bufonius | Juncus bufonius |
| Juncus bufonius var. bufonius | Juncus bufonius var. bufonius |
| Juncus bufonius var. congestus | Juncus bufonius var. congestus |
| Juncus bufonius var. occidentalis | Juncus bufonius var. occidentalis |
| Juncus capitatus | Juncus capitatus |
| Juncus effusus | Juncus effusus |
| Juncus effusus ssp. pacificus | Juncus effusus ssp. pacificus |
| Juncus gerardii | Juncus gerardii |
| Juncus gerardii ssp. gerardii | Juncus gerardii ssp. gerardii |
| Juncus kelloggii | Juncus kelloggii |
| Juncus lescurii | Juncus lescurii |
| Juncus mexicanus | Juncus mexicanus |
| Juncus oxymeris | Juncus oxymeris |
| Juncus patens | Juncus patens |
| Juncus phaeocephalus | Juncus phaeocephalus |
| Juncus phaeocephalus var. paniculatus | Juncus phaeocephalus var. paniculatus |
| Juncus tenuis | Juncus tenuis |
| Juncus uncialis | Juncus uncialis |
| Juncus xiphioides | Juncus xiphioides |
| Keckiella lemmonii | Keckiella lemmonii |
| Kickxia elatine | Kickxia elatine |
| Kickxia spuria | Kickxia spuria |
| Kochia scoparia | Kochia scoparia |
| Koeleria gerardi | Koeleria gerardi |
| Koeleria gerardii | Koeleria gerardii |
| Koeleria macrantha | Koeleria macrantha |
| Lactuca saligna | Lactuca saligna |
| Lactuca serriola | Lactuca serriola |
| Lagophylla ramosissima | Lagophylla ramosissima |
| Lamarckia aurea | Lamarckia aurea |
| Lamium amplexicaule | Lamium amplexicaule |
| Lantana montevidensis | Lantana montevidensis |
| Lasthenia californica | Lasthenia californica |
| Lasthenia californica ssp. californica | Lasthenia californica ssp. californica |
| Lasthenia chrysantha | Lasthenia chrysantha |
| Lasthenia conjugens | Lasthenia conjugens |
| Lasthenia ferrisiae | Lasthenia ferrisiae |
| Lasthenia fremontii | Lasthenia fremontii |
| Lasthenia glaberrima | Lasthenia glaberrima |
| Lasthenia glabrata | Lasthenia glabrata |
| Lasthenia glabrata ssp. glabrata | Lasthenia glabrata ssp. glabrata |
| Lasthenia gracilis | Lasthenia gracilis |
| Lasthenia microglossa | Lasthenia microglossa |
| Lasthenia minor | Lasthenia minor |
| Lasthenia platycarpha | Lasthenia platycarpha |
| Lathyrus jepsonii | Lathyrus jepsonii |
| Lathyrus jepsonii var. californicus | Lathyrus jepsonii var. californicus |
| Lathyrus jepsonii var. jepsonii | Lathyrus jepsonii var. jepsonii |
| Lathyrus sulphureus | Lathyrus sulphureus |
| Lathyrus tingitanus | Lathyrus tingitanus |
| Lathyrus vestitus | Lathyrus vestitus |
| Lathyrus vestitus var. vestitus | Lathyrus vestitus var. vestitus |
| Layia chrysanthemoides | Layia chrysanthemoides |
| Layia fremontii | Layia fremontii |
| Layia gaillardioides | Layia gaillardioides |
| Layia platyglossa | Layia platyglossa |
| Leersia oryzoides | Leersia oryzoides |
| Legenere limosa | Legenere limosa |
| Lemna minor | Lemna minor |
| Lemna minuta | Lemna minuta |
| Lemna turionifera | Lemna turionifera |
| Lemna valdiviana | Lemna valdiviana |
| Leontodon saxatilis | Leontodon saxatilis |
| Leontodon saxatilis ssp. longirostris | Leontodon saxatilis ssp. longirostris |
| Lepechinia calycina | Lepechinia calycina |
| Lepidium acutidens | Lepidium acutidens |
| Lepidium appelianum | Lepidium appelianum |
| Lepidium chalepense | Lepidium chalepense |
| Lepidium coronopus | Lepidium coronopus |
| Lepidium densiflorum | Lepidium densiflorum |
| Lepidium dictyotum | Lepidium dictyotum |
| Lepidium didymum | Lepidium didymum |
| Lepidium draba | Lepidium draba |
| Lepidium lasiocarpum | Lepidium lasiocarpum |
| Lepidium latifolium | Lepidium latifolium |
| Lepidium latipes | Lepidium latipes |
| Lepidium latipes var. heckardii | Lepidium latipes var. heckardii |
| Lepidium nitidum | Lepidium nitidum |
| Lepidium oxycarpum | Lepidium oxycarpum |
| Lepidium perfoliatum | Lepidium perfoliatum |
| Lepidium strictum | Lepidium strictum |
| Lepidium virginicum | Lepidium virginicum |
| Leptochloa fusca | Leptochloa fusca |
| Leptochloa fusca ssp. fascicularis | Leptochloa fusca ssp. fascicularis |
| Leptochloa fusca ssp. uninervia | Leptochloa fusca ssp. uninervia |
| Leptosiphon androsaceus | Leptosiphon androsaceus |
| Leptosiphon bicolor | Leptosiphon bicolor |
| Leptosiphon bolanderi | Leptosiphon bolanderi |
| Leptosiphon ciliatus | Leptosiphon ciliatus |
| Leptosiphon filipes | Leptosiphon filipes |
| Leptosiphon liniflorus | Leptosiphon liniflorus |
| Leptosiphon parviflorus | Leptosiphon parviflorus |
| Lessingia hololeuca | Lessingia hololeuca |
| Lessingia ramulosa | Lessingia ramulosa |
| Lessingia virgata | Lessingia virgata |
| Ligusticum apiifolium | Ligusticum apiifolium |
| Ligustrum lucidum | Ligustrum lucidum |
| Lilaeopsis masonii | Lilaeopsis masonii |
| Lilaeopsis occidentalis | Lilaeopsis occidentalis |
| Lilium rubescens | Lilium rubescens |
| Limnanthes alba | Limnanthes alba |
| Limnanthes douglasii | Limnanthes douglasii |
| Limnanthes douglasii ssp. nivea | Limnanthes douglasii ssp. nivea |
| Limnanthes douglasii ssp. rosea | Limnanthes douglasii ssp. rosea |
| Limonium californicum | Limonium californicum |
| Limonium ramosissimum | Limonium ramosissimum |
| Limosella acaulis | Limosella acaulis |
| Limosella aquatica | Limosella aquatica |
| Limosella australis | Limosella australis |
| Linanthus dichotomus | Linanthus dichotomus |
| Linaria dalmatica ssp. dalmatica | Linaria dalmatica ssp. dalmatica |
| Linaria genistifolia | Linaria genistifolia |
| Linaria maroccana | Linaria maroccana |
| Linum bienne | Linum bienne |
| Liquidambar styraciflua | Liquidambar styraciflua |
| Liriodendron tulipifera | Liriodendron tulipifera |
| Lithophragma affine | Lithophragma affine |
| Lithophragma bolanderi | Lithophragma bolanderi |
| Lithophragma campanulatum | Lithophragma campanulatum |
| Lithophragma heterophyllum | Lithophragma heterophyllum |
| Lobelia cardinalis | Lobelia cardinalis |
| Lobularia maritima | Lobularia maritima |
| Logfia filaginoides | Logfia filaginoides |
| Logfia gallica | Logfia gallica |
| Lolium rigidum | Lolium rigidum |
| Lomatium californicum | Lomatium californicum |
| Lomatium caruifolium | Lomatium caruifolium |
| Lomatium caruifolium var. caruifolium | Lomatium caruifolium var. caruifolium |
| Lomatium caruifolium var. denticulatum | Lomatium caruifolium var. denticulatum |
| Lomatium dasycarpum | Lomatium dasycarpum |
| Lomatium dasycarpum ssp. dasycarpum | Lomatium dasycarpum ssp. dasycarpum |
| Lomatium dasycarpum ssp. tomentosum | Lomatium dasycarpum ssp. tomentosum |
| Lomatium macrocarpum | Lomatium macrocarpum |
| Lomatium marginatum | Lomatium marginatum |
| Lomatium marginatum var. marginatum | Lomatium marginatum var. marginatum |
| Lomatium nudicaule | Lomatium nudicaule |
| Lomatium repostum | Lomatium repostum |
| Lomatium utriculatum | Lomatium utriculatum |
| Lonicera hispidula | Lonicera hispidula |
| Lonicera interrupta | Lonicera interrupta |
| Lonicera involucrata | Lonicera involucrata |
| Lotus corniculatus | Lotus corniculatus |
| Lotus tenuis | Lotus tenuis |
| Ludwigia hexapetala | Ludwigia hexapetala |
| Ludwigia palustris | Ludwigia palustris |
| Ludwigia peploides | Ludwigia peploides |
| Ludwigia peploides ssp. montevidensis | Ludwigia peploides ssp. montevidensis |
| Ludwigia peploides ssp. peploides | Ludwigia peploides ssp. peploides |
| Lunaria annua | Lunaria annua |
| Lupinus affinis | Lupinus affinis |
| Lupinus albifrons | Lupinus albifrons |
| Lupinus albifrons var. albifrons | Lupinus albifrons var. albifrons |
| Lupinus arboreus | Lupinus arboreus |
| Lupinus benthamii | Lupinus benthamii |
| Lupinus bicolor | Lupinus bicolor |
| Lupinus formosus | Lupinus formosus |
| Lupinus formosus var. formosus | Lupinus formosus var. formosus |
| Lupinus formosus var. robustus | Lupinus formosus var. robustus |
| Lupinus latifolius | Lupinus latifolius |
| Lupinus latifolius var. latifolius | Lupinus latifolius var. latifolius |
| Lupinus luteolus | Lupinus luteolus |
| Lupinus microcarpus | Lupinus microcarpus |
| Lupinus microcarpus var. densiflorus | Lupinus microcarpus var. densiflorus |
| Lupinus microcarpus var. microcarpus | Lupinus microcarpus var. microcarpus |
| Lupinus nanus | Lupinus nanus |
| Lupinus pachylobus | Lupinus pachylobus |
| Lupinus rivularis | Lupinus rivularis |
| Lupinus succulentus | Lupinus succulentus |
| Luzula comosa | Luzula comosa |
| Luzula subsessilis | Luzula subsessilis |
| Lycopus americanus | Lycopus americanus |
| Lycopus asper | Lycopus asper |
| Lysimachia arvensis | Lysimachia arvensis |
| Lysimachia maritima | Lysimachia maritima |
| Lysimachia minima | Lysimachia minima |
| Lythrum californicum | Lythrum californicum |
| Lythrum hyssopifolia | Lythrum hyssopifolia |
| Lythrum salicaria | Lythrum salicaria |
| Lythrum tribracteatum | Lythrum tribracteatum |
| Maclura pomifera | Maclura pomifera |
| Madia citriodora | Madia citriodora |
| Madia elegans | Madia elegans |
| Madia exigua | Madia exigua |
| Madia gracilis | Madia gracilis |
| Madia radiata | Madia radiata |
| Madia sativa | Madia sativa |
| Malacothrix clevelandii | Malacothrix clevelandii |
| Malacothrix floccifera | Malacothrix floccifera |
| Malva assurgentiflora | Malva assurgentiflora |
| Malva multiflora | Malva multiflora |
| Malva neglecta | Malva neglecta |
| Malva nicaeensis | Malva nicaeensis |
| Malva parviflora | Malva parviflora |
| Malvella leprosa | Malvella leprosa |
| Marah fabacea | Marah fabacea |
| Marah oregana | Marah oregana |
| Marah watsonii | Marah watsonii |
| Marrubium vulgare | Marrubium vulgare |
| Marsilea vestita | Marsilea vestita |
| Marsilea vestita ssp. vestita | Marsilea vestita ssp. vestita |
| Matricaria chamomilla | Matricaria chamomilla |
| Matricaria discoidea | Matricaria discoidea |
| Matricaria occidentalis | Matricaria occidentalis |
| Medicago lupulina | Medicago lupulina |
| Medicago orbicularis | Medicago orbicularis |
| Medicago polymorpha | Medicago polymorpha |
| Medicago sativa | Medicago sativa |
| Melaleuca viminalis | Melaleuca viminalis |
| Melica californica | Melica californica |
| Melica harfordii | Melica harfordii |
| Melica imperfecta | Melica imperfecta |
| Melica torreyana | Melica torreyana |
| Melilotus albus | Melilotus albus |
| Melilotus indicus | Melilotus indicus |
| Melilotus officinalis | Melilotus officinalis |
| Mentha aquatica | Mentha aquatica |
| Mentha arvensis | Mentha arvensis |
| Mentha canadensis | Mentha canadensis |
| Mentha pulegium | Mentha pulegium |
| Mentha spicata | Mentha spicata |
| Mentha Xpiperita | Mentha Xpiperita |
| Mentzelia affinis | Mentzelia affinis |
| Mentzelia dispersa | Mentzelia dispersa |
| Mentzelia laevicaulis | Mentzelia laevicaulis |
| Mentzelia lindleyi | Mentzelia lindleyi |
| Mesembryanthemum nodiflorum | Mesembryanthemum nodiflorum |
| Micranthes californica | Micranthes californica |
| Micranthes integrifolia | Micranthes integrifolia |
| Micropus amphibolus | Micropus amphibolus |
| Micropus californicus | Micropus californicus |
| Micropus californicus var. californicus | Micropus californicus var. californicus |
| Micropus californicus var. subvestitus | Micropus californicus var. subvestitus |
| Microseris acuminata | Microseris acuminata |
| Microseris campestris | Microseris campestris |
| Microseris douglasii | Microseris douglasii |
| Microseris douglasii ssp. douglasii | Microseris douglasii ssp. douglasii |
| Microseris douglasii ssp. tenella | Microseris douglasii ssp. tenella |
| Microseris elegans | Microseris elegans |
| Microseris paludosa | Microseris paludosa |
| Microseris sylvatica | Microseris sylvatica |
| Microsteris gracilis | Microsteris gracilis |
| Mimetanthe pilosa | Mimetanthe pilosa |
| Mollugo verticillata | Mollugo verticillata |
| Monardella sheltonii | Monardella sheltonii |
| Monardella villosa | Monardella villosa |
| Monardella villosa ssp. villosa | Monardella villosa ssp. villosa |
| Monardella viridis | Monardella viridis |
| Monolopia major | Monolopia major |
| Montia fontana | Montia fontana |
| Morus alba | Morus alba |
| Muhlenbergia glauca | Muhlenbergia glauca |
| Muilla maritima | Muilla maritima |
| Myoporum laetum | Myoporum laetum |
| Myosurus minimus | Myosurus minimus |
| Myosurus minimus ssp. apus | Myosurus minimus ssp. apus |
| Myosurus sessilis | Myosurus sessilis |
| Myriophyllum aquaticum | Myriophyllum aquaticum |
| Myriophyllum sibiricum | Myriophyllum sibiricum |
| Myriophyllum spicatum | Myriophyllum spicatum |
| Nandina domestica | Nandina domestica |
| Nasturtium officinale | Nasturtium officinale |
| Navarretia cotulifolia | Navarretia cotulifolia |
| Navarretia eriocephala | Navarretia eriocephala |
| Navarretia heterandra | Navarretia heterandra |
| Navarretia intertexta | Navarretia intertexta |
| Navarretia leucocephala | Navarretia leucocephala |
| Navarretia leucocephala ssp. bakeri | Navarretia leucocephala ssp. bakeri |
| Navarretia leucocephala ssp. leucocephala | Navarretia leucocephala ssp. leucocephala |
| Navarretia leucocephala ssp. minima | Navarretia leucocephala ssp. minima |
| Navarretia mellita | Navarretia mellita |
| Navarretia pubescens | Navarretia pubescens |
| Navarretia tagetina | Navarretia tagetina |
| Navarretia viscidula | Navarretia viscidula |
| Nemophila heterophylla | Nemophila heterophylla |
| Nemophila menziesii | Nemophila menziesii |
| Nemophila parviflora | Nemophila parviflora |
| Nemophila pedunculata | Nemophila pedunculata |
| Neostapfia colusana | Neostapfia colusana |
| Nepeta cataria | Nepeta cataria |
| Nerium oleander | Nerium oleander |
| Nicandra physalodes | Nicandra physalodes |
| Nicotiana glauca | Nicotiana glauca |
| Nicotiana quadrivalvis | Nicotiana quadrivalvis |
| Nitrophila occidentalis | Nitrophila occidentalis |
| Nuttallanthus texanus | Nuttallanthus texanus |
| Oemleria cerasiformis | Oemleria cerasiformis |
| Oenanthe sarmentosa | Oenanthe sarmentosa |
| Oenothera deltoides | Oenothera deltoides |
| Oenothera deltoides ssp. howellii | Oenothera deltoides ssp. howellii |
| Oenothera elata | Oenothera elata |
| Oenothera elata ssp. hookeri | Oenothera elata ssp. hookeri |
| Olea europaea | Olea europaea |
| Orcuttia inaequalis | Orcuttia inaequalis |
| Orobanche aegyptiaca | Orobanche aegyptiaca |
| Osmorhiza berteroi | Osmorhiza berteroi |
| Other | Other |
| Oxalis californica | Oxalis californica |
| Oxalis corniculata | Oxalis corniculata |
| Oxalis pes-caprae | Oxalis pes-caprae |
| Panicum capillare | Panicum capillare |
| Panicum dichotomiflorum | Panicum dichotomiflorum |
| Panicum hillmanii | Panicum hillmanii |
| Parapholis incurva | Parapholis incurva |
| Parentucellia viscosa | Parentucellia viscosa |
| Parietaria judaica | Parietaria judaica |
| Parthenocissus inserta | Parthenocissus inserta |
| Paspalum dilatatum | Paspalum dilatatum |
| Paspalum distichum | Paspalum distichum |
| Pedicularis densiflora | Pedicularis densiflora |
| Pelargonium grossularioides | Pelargonium grossularioides |
| Pelargonium peltatum | Pelargonium peltatum |
| Pellaea andromedifolia | Pellaea andromedifolia |
| Pellaea mucronata | Pellaea mucronata |
| Pennisetum clandestinum | Pennisetum clandestinum |
| Pennisetum setaceum | Pennisetum setaceum |
| Penstemon heterophyllus | Penstemon heterophyllus |
| Penstemon heterophyllus var. purdyi | Penstemon heterophyllus var. purdyi |
| Pentagramma triangularis | Pentagramma triangularis |
| Pentagramma triangularis ssp. triangularis | Pentagramma triangularis ssp. triangularis |
| Perideridia gairdneri | Perideridia gairdneri |
| Perideridia gairdneri ssp. gairdneri | Perideridia gairdneri ssp. gairdneri |
| Perideridia kelloggii | Perideridia kelloggii |
| Peritoma arborea | Peritoma arborea |
| Persicaria amphibia | Persicaria amphibia |
| Persicaria capitata | Persicaria capitata |
| Persicaria hydropiper | Persicaria hydropiper |
| Persicaria hydropiperoides | Persicaria hydropiperoides |
| Persicaria lapathifolia | Persicaria lapathifolia |
| Persicaria maculosa | Persicaria maculosa |
| Persicaria punctata | Persicaria punctata |
| Petrorhagia dubia | Petrorhagia dubia |
| Phacelia ciliata | Phacelia ciliata |
| Phacelia ciliata var. ciliata | Phacelia ciliata var. ciliata |
| Phacelia distans | Phacelia distans |
| Phacelia egena | Phacelia egena |
| Phacelia heterophylla | Phacelia heterophylla |
| Phacelia heterophylla var. virgata | Phacelia heterophylla var. virgata |
| Phacelia humilis | Phacelia humilis |
| Phacelia humilis var. humilis | Phacelia humilis var. humilis |
| Phacelia imbricata | Phacelia imbricata |
| Phacelia nemoralis | Phacelia nemoralis |
| Phacelia suaveolens | Phacelia suaveolens |
| Phacelia tanacetifolia | Phacelia tanacetifolia |
| Phalaris angusta | Phalaris angusta |
| Phalaris aquatica | Phalaris aquatica |
| Phalaris arundinacea | Phalaris arundinacea |
| Phalaris brachystachys | Phalaris brachystachys |
| Phalaris canariensis | Phalaris canariensis |
| Phalaris caroliniana | Phalaris caroliniana |
| Phalaris lemmonii | Phalaris lemmonii |
| Phalaris minor | Phalaris minor |
| Phalaris paradoxa | Phalaris paradoxa |
| Phleum pratense | Phleum pratense |
| Phoenix canariensis | Phoenix canariensis |
| Phoradendron juniperinum | Phoradendron juniperinum |
| Phoradendron leucarpum | Phoradendron leucarpum |
| Phoradendron leucarpum ssp. macrophyllum | Phoradendron leucarpum ssp. macrophyllum |
| Phoradendron leucarpum ssp. tomentosum | Phoradendron leucarpum ssp. tomentosum |
| Phragmites australis | Phragmites australis |
| Phyla caespitosa | Phyla caespitosa |
| Phyla lanceolata | Phyla lanceolata |
| Phyla nodiflora | Phyla nodiflora |
| Physalis lanceifolia | Physalis lanceifolia |
| Phytolacca americana | Phytolacca americana |
| Phytolacca icosandra | Phytolacca icosandra |
| Pickeringia montana | Pickeringia montana |
| Pickeringia montana var. montana | Pickeringia montana var. montana |
| Pilularia americana | Pilularia americana |
| Pinus canariensis | Pinus canariensis |
| Pinus halepensis | Pinus halepensis |
| Pinus pinea | Pinus pinea |
| Pinus ponderosa | Pinus ponderosa |
| Pinus radiata | Pinus radiata |
| Pinus sabiniana | Pinus sabiniana |
| Piperia elegans | Piperia elegans |
| Piperia elongata | Piperia elongata |
| Pistacia atlantica | Pistacia atlantica |
| Pistacia chinensis | Pistacia chinensis |
| Pisum sativum | Pisum sativum |
| Pittosporum undulatum | Pittosporum undulatum |
| Plagiobothrys acanthocarpus | Plagiobothrys acanthocarpus |
| Plagiobothrys bracteatus | Plagiobothrys bracteatus |
| Plagiobothrys canescens | Plagiobothrys canescens |
| Plagiobothrys chorisianus | Plagiobothrys chorisianus |
| Plagiobothrys cusickii | Plagiobothrys cusickii |
| Plagiobothrys fulvus | Plagiobothrys fulvus |
| Plagiobothrys fulvus var. campestris | Plagiobothrys fulvus var. campestris |
| Plagiobothrys greenei | Plagiobothrys greenei |
| Plagiobothrys humistratus | Plagiobothrys humistratus |
| Plagiobothrys hystriculus | Plagiobothrys hystriculus |
| Plagiobothrys leptocladus | Plagiobothrys leptocladus |
| Plagiobothrys nothofulvus | Plagiobothrys nothofulvus |
| Plagiobothrys stipitatus | Plagiobothrys stipitatus |
| Plagiobothrys stipitatus var. micranthus | Plagiobothrys stipitatus var. micranthus |
| Plagiobothrys stipitatus var. stipitatus | Plagiobothrys stipitatus var. stipitatus |
| Plagiobothrys tenellus | Plagiobothrys tenellus |
| Plagiobothrys tener | Plagiobothrys tener |
| Plagiobothrys tener var. tener | Plagiobothrys tener var. tener |
| Plagiobothrys trachycarpus | Plagiobothrys trachycarpus |
| Plagiobothrys undulatus | Plagiobothrys undulatus |
| Planodes virginicum | Planodes virginicum |
| Plantago coronopus | Plantago coronopus |
| Plantago elongata | Plantago elongata |
| Plantago erecta | Plantago erecta |
| Plantago lanceolata | Plantago lanceolata |
| Plantago major | Plantago major |
| Plantago maritima | Plantago maritima |
| Plantago pusilla | Plantago pusilla |
| Plantago subnuda | Plantago subnuda |
| Platanus racemosa | Platanus racemosa |
| Platystemon californicus | Platystemon californicus |
| Plectritis ciliosa | Plectritis ciliosa |
| Plectritis congesta | Plectritis congesta |
| Plectritis congesta ssp. brachystemon | Plectritis congesta ssp. brachystemon |
| Plectritis macrocera | Plectritis macrocera |
| Pleuropogon californicus | Pleuropogon californicus |
| Pleuropogon californicus var. californicus | Pleuropogon californicus var. californicus |
| Pluchea odorata | Pluchea odorata |
| Pluchea odorata var. odorata | Pluchea odorata var. odorata |
| Poa annua | Poa annua |
| Poa bulbosa | Poa bulbosa |
| Poa howellii | Poa howellii |
| Poa pratensis | Poa pratensis |
| Poa pratensis ssp. pratensis | Poa pratensis ssp. pratensis |
| Poa secunda | Poa secunda |
| Poa secunda ssp. juncifolia | Poa secunda ssp. juncifolia |
| Poa secunda ssp. secunda | Poa secunda ssp. secunda |
| Poa unilateralis | Poa unilateralis |
| Poa unilateralis ssp. unilateralis | Poa unilateralis ssp. unilateralis |
| Pogogyne douglasii | Pogogyne douglasii |
| Pogogyne douglasii ssp. parviflora | Pogogyne douglasii ssp. parviflora |
| Pogogyne zizyphoroides | Pogogyne zizyphoroides |
| Polycarpon tetraphyllum | Polycarpon tetraphyllum |
| Polygala myrtifolia | Polygala myrtifolia |
| Polygonum argyrocoleon | Polygonum argyrocoleon |
| Polygonum aviculare | Polygonum aviculare |
| Polygonum aviculare ssp. aviculare | Polygonum aviculare ssp. aviculare |
| Polygonum aviculare ssp. buxiforme | Polygonum aviculare ssp. buxiforme |
| Polygonum aviculare ssp. depressum | Polygonum aviculare ssp. depressum |
| Polygonum bolanderi | Polygonum bolanderi |
| Polygonum marinense | Polygonum marinense |
| Polygonum paronychia | Polygonum paronychia |
| Polygonum ramosissimum | Polygonum ramosissimum |
| Polypodium californicum | Polypodium californicum |
| Polypodium calirhiza | Polypodium calirhiza |
| Polypogon interruptus | Polypogon interruptus |
| Polypogon maritimus | Polypogon maritimus |
| Polypogon monspeliensis | Polypogon monspeliensis |
| Polypogon viridis | Polypogon viridis |
| Polystichum munitum | Polystichum munitum |
| Populus fremontii | Populus fremontii |
| Populus fremontii ssp. fremontii | Populus fremontii ssp. fremontii |
| Populus nigra | Populus nigra |
| Portulaca oleracea | Portulaca oleracea |
| Potamogeton crispus | Potamogeton crispus |
| Potamogeton illinoensis | Potamogeton illinoensis |
| Potamogeton nodosus | Potamogeton nodosus |
| Potentilla anserina | Potentilla anserina |
| Potentilla anserina ssp. pacifica | Potentilla anserina ssp. pacifica |
| Potentilla rivalis | Potentilla rivalis |
| Primula clevelandii | Primula clevelandii |
| Primula clevelandii var. patula | Primula clevelandii var. patula |
| Primula hendersonii | Primula hendersonii |
| Proboscidea louisianica | Proboscidea louisianica |
| Proboscidea louisianica ssp. louisianica | Proboscidea louisianica ssp. louisianica |
| Proboscidea lutea | Proboscidea lutea |
| Prosartes hookeri | Prosartes hookeri |
| Prunella vulgaris | Prunella vulgaris |
| Prunella vulgaris var. lanceolata | Prunella vulgaris var. lanceolata |
| Prunus armeniaca | Prunus armeniaca |
| Prunus cerasifera | Prunus cerasifera |
| Prunus dulcis | Prunus dulcis |
| Prunus ilicifolia | Prunus ilicifolia |
| Prunus ilicifolia ssp. ilicifolia | Prunus ilicifolia ssp. ilicifolia |
| Prunus subcordata | Prunus subcordata |
| Prunus virginiana | Prunus virginiana |
| Prunus virginiana var. demissa | Prunus virginiana var. demissa |
| Pseudognaphalium beneolens | Pseudognaphalium beneolens |
| Pseudognaphalium californicum | Pseudognaphalium californicum |
| Pseudognaphalium canescens | Pseudognaphalium canescens |
| Pseudognaphalium luteoalbum | Pseudognaphalium luteoalbum |
| Pseudognaphalium ramosissimum | Pseudognaphalium ramosissimum |
| Pseudognaphalium stramineum | Pseudognaphalium stramineum |
| Psilocarphus brevissimus | Psilocarphus brevissimus |
| Psilocarphus brevissimus var. brevissimus | Psilocarphus brevissimus var. brevissimus |
| Psilocarphus brevissimus var. multiflorus | Psilocarphus brevissimus var. multiflorus |
| Psilocarphus chilensis | Psilocarphus chilensis |
| Psilocarphus oregonus | Psilocarphus oregonus |
| Psilocarphus tenellus | Psilocarphus tenellus |
| Ptelea crenulata | Ptelea crenulata |
| Pteridium aquilinum | Pteridium aquilinum |
| Pterostegia drymarioides | Pterostegia drymarioides |
| Puccinellia nutkaensis | Puccinellia nutkaensis |
| Puccinellia nuttalliana | Puccinellia nuttalliana |
| Puccinellia simplex | Puccinellia simplex |
| Punica granatum | Punica granatum |
| Pyracantha angustifolia | Pyracantha angustifolia |
| Pyracantha coccinea | Pyracantha coccinea |
| Pyracantha crenulata | Pyracantha crenulata |
| Pyrrocoma racemosa | Pyrrocoma racemosa |
| Pyrrocoma racemosa var. racemosa | Pyrrocoma racemosa var. racemosa |
| Pyrus calleryana | Pyrus calleryana |
| Pyrus communis | Pyrus communis |
| Quercus agrifolia | Quercus agrifolia |
| Quercus agrifolia var. agrifolia | Quercus agrifolia var. agrifolia |
| Quercus berberidifolia | Quercus berberidifolia |
| Quercus chrysolepis | Quercus chrysolepis |
| Quercus douglasii | Quercus douglasii |
| Quercus dumosa | Quercus dumosa |
| Quercus durata | Quercus durata |
| Quercus garryana | Quercus garryana |
| Quercus ilex | Quercus ilex |
| Quercus kelloggii | Quercus kelloggii |
| Quercus lobata | Quercus lobata |
| Quercus parvula | Quercus parvula |
| Quercus parvula var. shrevei | Quercus parvula var. shrevei |
| Quercus suber | Quercus suber |
| Quercus wislizeni | Quercus wislizeni |
| Quercus wislizeni var. frutescens | Quercus wislizeni var. frutescens |
| Quercus wislizeni var. wislizeni | Quercus wislizeni var. wislizeni |
| Quercus Xmorehus | Quercus Xmorehus |
| Rafinesquia californica | Rafinesquia californica |
| Ranunculus aquatilis | Ranunculus aquatilis |
| Ranunculus aquatilis var. aquatilis | Ranunculus aquatilis var. aquatilis |
| Ranunculus aquatilis var. diffusus | Ranunculus aquatilis var. diffusus |
| Ranunculus bulbosus | Ranunculus bulbosus |
| Ranunculus californicus | Ranunculus californicus |
| Ranunculus canus | Ranunculus canus |
| Ranunculus canus var. canus | Ranunculus canus var. canus |
| Ranunculus hebecarpus | Ranunculus hebecarpus |
| Ranunculus lobbii | Ranunculus lobbii |
| Ranunculus muricatus | Ranunculus muricatus |
| Ranunculus occidentalis | Ranunculus occidentalis |
| Ranunculus occidentalis var. occidentalis | Ranunculus occidentalis var. occidentalis |
| Ranunculus orthorhynchus | Ranunculus orthorhynchus |
| Ranunculus orthorhynchus var. bloomeri | Ranunculus orthorhynchus var. bloomeri |
| Ranunculus parviflorus | Ranunculus parviflorus |
| Raphanus raphanistrum | Raphanus raphanistrum |
| Raphanus sativus | Raphanus sativus |
| Rhagadiolus stellatus | Rhagadiolus stellatus |
| Rhamnus alaternus | Rhamnus alaternus |
| Rhamnus crocea | Rhamnus crocea |
| Rhamnus ilicifolia | Rhamnus ilicifolia |
| Rhaponticum repens | Rhaponticum repens |
| Rhododendron occidentale | Rhododendron occidentale |
| Rhododendron occidentale var. occidentale | Rhododendron occidentale var. occidentale |
| Rhus aromatica | Rhus aromatica |
| Rhynchospora californica | Rhynchospora californica |
| Ribes aureum | Ribes aureum |
| Ribes californicum | Ribes californicum |
| Ribes californicum var. californicum | Ribes californicum var. californicum |
| Ribes malvaceum | Ribes malvaceum |
| Ribes menziesii | Ribes menziesii |
| Ribes menziesii var. menziesii | Ribes menziesii var. menziesii |
| Ribes sanguineum | Ribes sanguineum |
| Ribes sanguineum var. glutinosum | Ribes sanguineum var. glutinosum |
| Ribes speciosum | Ribes speciosum |
| Ribes victoris | Ribes victoris |
| Rigiopappus leptocladus | Rigiopappus leptocladus |
| Robinia pseudoacacia | Robinia pseudoacacia |
| Romulea rosea | Romulea rosea |
| Rorippa curvisiliqua | Rorippa curvisiliqua |
| Rorippa palustris | Rorippa palustris |
| Rorippa palustris ssp. palustris | Rorippa palustris ssp. palustris |
| Rosa californica | Rosa californica |
| Rosa gymnocarpa | Rosa gymnocarpa |
| Rosa spithamea | Rosa spithamea |
| Rosmarinus officinalis | Rosmarinus officinalis |
| Rotala ramosior | Rotala ramosior |
| Rubus armeniacus | Rubus armeniacus |
| Rubus parviflorus | Rubus parviflorus |
| Rubus ulmifolius | Rubus ulmifolius |
| Rubus ursinus | Rubus ursinus |
| Rumex acetosella | Rumex acetosella |
| Rumex californicus | Rumex californicus |
| Rumex conglomeratus | Rumex conglomeratus |
| Rumex crassus | Rumex crassus |
| Rumex crispus | Rumex crispus |
| Rumex dentatus | Rumex dentatus |
| Rumex fueginus | Rumex fueginus |
| Rumex obtusifolius | Rumex obtusifolius |
| Rumex occidentalis | Rumex occidentalis |
| Rumex persicarioides | Rumex persicarioides |
| Rumex pulcher | Rumex pulcher |
| Rumex salicifolius | Rumex salicifolius |
| Rumex stenophyllus | Rumex stenophyllus |
| Rumex transitorius | Rumex transitorius |
| Rumex violascens | Rumex violascens |
| Rupertia physodes | Rupertia physodes |
| Ruppia cirrhosa | Ruppia cirrhosa |
| Ruppia maritima | Ruppia maritima |
| Sabulina californica | Sabulina californica |
| Sabulina douglasii | Sabulina douglasii |
| Sagina apetala | Sagina apetala |
| Sagina decumbens | Sagina decumbens |
| Sagina decumbens ssp. occidentalis | Sagina decumbens ssp. occidentalis |
| Sagina saginoides | Sagina saginoides |
| Sagittaria latifolia | Sagittaria latifolia |
| Sagittaria sanfordii | Sagittaria sanfordii |
| Salicornia depressa | Salicornia depressa |
| Salicornia pacifica | Salicornia pacifica |
| Salix babylonica | Salix babylonica |
| Salix breweri | Salix breweri |
| Salix exigua | Salix exigua |
| Salix exigua var. hindsiana | Salix exigua var. hindsiana |
| Salix gooddingii | Salix gooddingii |
| Salix laevigata | Salix laevigata |
| Salix lasiandra | Salix lasiandra |
| Salix lasiandra var. lasiandra | Salix lasiandra var. lasiandra |
| Salix lasiolepis | Salix lasiolepis |
| Salix melanopsis | Salix melanopsis |
| Salix scouleriana | Salix scouleriana |
| Salpichroa origanifolia | Salpichroa origanifolia |
| Salsola soda | Salsola soda |
| Salsola tragus | Salsola tragus |
| Salvia columbariae | Salvia columbariae |
| Salvia spathacea | Salvia spathacea |
| Sambucus mexicana | Sambucus mexicana |
| Sambucus nigra | Sambucus nigra |
| Samolus parviflorus | Samolus parviflorus |
| Sanicula bipinnata | Sanicula bipinnata |
| Sanicula bipinnatifida | Sanicula bipinnatifida |
| Sanicula crassicaulis | Sanicula crassicaulis |
| Sanicula graveolens | Sanicula graveolens |
| Sanicula tuberosa | Sanicula tuberosa |
| Scabiosa atropurpurea | Scabiosa atropurpurea |
| Scandix pecten-veneris | Scandix pecten-veneris |
| Schinus molle | Schinus molle |
| Schinus terebinthifolius | Schinus terebinthifolius |
| Schismus arabicus | Schismus arabicus |
| Schizachyrium scoparium | Schizachyrium scoparium |
| Schoenoplectus acutus | Schoenoplectus acutus |
| Schoenoplectus acutus var. occidentalis | Schoenoplectus acutus var. occidentalis |
| Schoenoplectus americanus | Schoenoplectus americanus |
| Schoenoplectus californicus | Schoenoplectus californicus |
| Schoenoplectus pungens | Schoenoplectus pungens |
| Schoenoplectus pungens var. longispicatus | Schoenoplectus pungens var. longispicatus |
| Schoenoplectus tabernaemontani | Schoenoplectus tabernaemontani |
| Scirpus microcarpus | Scirpus microcarpus |
| Scolymus hispanicus | Scolymus hispanicus |
| Scribneria bolanderi | Scribneria bolanderi |
| Scrophularia californica | Scrophularia californica |
| Scutellaria californica | Scutellaria californica |
| Scutellaria tuberosa | Scutellaria tuberosa |
| Sedella pumila | Sedella pumila |
| Sedum spathulifolium | Sedum spathulifolium |
| Selaginella wallacei | Selaginella wallacei |
| Senecio aronicoides | Senecio aronicoides |
| Senecio flaccidus | Senecio flaccidus |
| Senecio flaccidus var. douglasii | Senecio flaccidus var. douglasii |
| Senecio hydrophiloides | Senecio hydrophiloides |
| Senecio hydrophilus | Senecio hydrophilus |
| Senecio sylvaticus | Senecio sylvaticus |
| Senecio vulgaris | Senecio vulgaris |
| Sesbania punicea | Sesbania punicea |
| Sesuvium verrucosum | Sesuvium verrucosum |
| Setaria faberi | Setaria faberi |
| Setaria parviflora | Setaria parviflora |
| Setaria pumila | Setaria pumila |
| Setaria pumila ssp. pumila | Setaria pumila ssp. pumila |
| Setaria sphacelata | Setaria sphacelata |
| Setaria verticillata | Setaria verticillata |
| Setaria viridis | Setaria viridis |
| Sherardia arvensis | Sherardia arvensis |
| Sidalcea diploscypha | Sidalcea diploscypha |
| Sidalcea hickmanii | Sidalcea hickmanii |
| Sidalcea hickmanii ssp. napensis | Sidalcea hickmanii ssp. napensis |
| Sidalcea hickmanii ssp. viridis | Sidalcea hickmanii ssp. viridis |
| Sidalcea hirsuta | Sidalcea hirsuta |
| Sidalcea keckii | Sidalcea keckii |
| Sidalcea malviflora | Sidalcea malviflora |
| Sidalcea malviflora ssp. laciniata | Sidalcea malviflora ssp. laciniata |
| Sidalcea malviflora ssp. malviflora | Sidalcea malviflora ssp. malviflora |
| Silene antirrhina | Silene antirrhina |
| Silene gallica | Silene gallica |
| Silene laciniata | Silene laciniata |
| Silene laciniata ssp. californica | Silene laciniata ssp. californica |
| Silene vulgaris | Silene vulgaris |
| Silybum marianum | Silybum marianum |
| Sinapis alba | Sinapis alba |
| Sinapis arvensis | Sinapis arvensis |
| Sisymbrium altissimum | Sisymbrium altissimum |
| Sisymbrium officinale | Sisymbrium officinale |
| Sisymbrium orientale | Sisymbrium orientale |
| Sisyrinchium bellum | Sisyrinchium bellum |
| Sium suave | Sium suave |
| Solanum americanum | Solanum americanum |
| Solanum aviculare | Solanum aviculare |
| Solanum elaeagnifolium | Solanum elaeagnifolium |
| Solanum laciniatum | Solanum laciniatum |
| Solanum lanceolatum | Solanum lanceolatum |
| Solanum parishii | Solanum parishii |
| Solanum physalifolium | Solanum physalifolium |
| Solanum umbelliferum | Solanum umbelliferum |
| Solanum xanti | Solanum xanti |
| Solidago canadensis | Solidago canadensis |
| Solidago elongata | Solidago elongata |
| Solidago velutina | Solidago velutina |
| Solidago velutina ssp. californica | Solidago velutina ssp. californica |
| Soliva sessilis | Soliva sessilis |
| Sonchus asper | Sonchus asper |
| Sonchus asper ssp. asper | Sonchus asper ssp. asper |
| Sonchus oleraceus | Sonchus oleraceus |
| Sonchus tenerrimus | Sonchus tenerrimus |
| Sorghum bicolor | Sorghum bicolor |
| Sorghum halepense | Sorghum halepense |
| Spartina alterniflora | Spartina alterniflora |
| Spartina alterniflora X Spartina foliosa | Spartina alterniflora X Spartina foliosa |
| Spartina densiflora | Spartina densiflora |
| Spartina foliosa | Spartina foliosa |
| Spartina patens | Spartina patens |
| Spartium junceum | Spartium junceum |
| Spergula arvensis | Spergula arvensis |
| Spergularia atrosperma | Spergularia atrosperma |
| Spergularia bocconi | Spergularia bocconi |
| Spergularia macrotheca | Spergularia macrotheca |
| Spergularia macrotheca var. leucantha | Spergularia macrotheca var. leucantha |
| Spergularia macrotheca var. longistyla | Spergularia macrotheca var. longistyla |
| Spergularia marina | Spergularia marina |
| Spergularia media | Spergularia media |
| Spergularia platensis | Spergularia platensis |
| Spergularia rubra | Spergularia rubra |
| Spergularia villosa | Spergularia villosa |
| Sporobolus airoides | Sporobolus airoides |
| Sporobolus cryptandrus | Sporobolus cryptandrus |
| Sporobolus indicus | Sporobolus indicus |
| Stachys ajugoides | Stachys ajugoides |
| Stachys albens | Stachys albens |
| Stachys bullata | Stachys bullata |
| Stachys pycnantha | Stachys pycnantha |
| Stachys rigida | Stachys rigida |
| Stachys rigida var. quercetorum | Stachys rigida var. quercetorum |
| Stebbinsoseris heterocarpa | Stebbinsoseris heterocarpa |
| Stellaria longipes | Stellaria longipes |
| Stellaria media | Stellaria media |
| Stellaria nitens | Stellaria nitens |
| Stellaria umbellata | Stellaria umbellata |
| Stenotaphrum secundatum | Stenotaphrum secundatum |
| Stephanomeria virgata | Stephanomeria virgata |
| Stephanomeria virgata ssp. pleurocarpa | Stephanomeria virgata ssp. pleurocarpa |
| Stephanomeria virgata ssp. virgata | Stephanomeria virgata ssp. virgata |
| Stipa cernua | Stipa cernua |
| Stipa lepida | Stipa lepida |
| Stipa miliacea | Stipa miliacea |
| Stipa miliacea var. miliacea | Stipa miliacea var. miliacea |
| Stipa pulchra | Stipa pulchra |
| Streptanthus glandulosus | Streptanthus glandulosus |
| Streptanthus glandulosus ssp. glandulosus | Streptanthus glandulosus ssp. glandulosus |
| Streptanthus tortuosus | Streptanthus tortuosus |
| Stuckenia filiformis | Stuckenia filiformis |
| Stuckenia filiformis ssp. alpina | Stuckenia filiformis ssp. alpina |
| Stuckenia pectinata | Stuckenia pectinata |
| Suaeda calceoliformis | Suaeda calceoliformis |
| Suaeda nigra | Suaeda nigra |
| Symphoricarpos albus | Symphoricarpos albus |
| Symphoricarpos albus var. laevigatus | Symphoricarpos albus var. laevigatus |
| Symphoricarpos mollis | Symphoricarpos mollis |
| Symphyotrichum chilense | Symphyotrichum chilense |
| Symphyotrichum lentum | Symphyotrichum lentum |
| Symphyotrichum spathulatum | Symphyotrichum spathulatum |
| Symphyotrichum subspicatum | Symphyotrichum subspicatum |
| Symphyotrichum subulatum | Symphyotrichum subulatum |
| Symphyotrichum subulatum var. elongatum | Symphyotrichum subulatum var. elongatum |
| Symphyotrichum subulatum var. parviflorum | Symphyotrichum subulatum var. parviflorum |
| Symphyotrichum subulatum var. squamatum | Symphyotrichum subulatum var. squamatum |
| Tamarix parviflora | Tamarix parviflora |
| Tamarix ramosissima | Tamarix ramosissima |
| Taraxacum officinale | Taraxacum officinale |
| Taraxia ovata | Taraxia ovata |
| Tetragonia tetragonoides | Tetragonia tetragonoides |
| Thysanocarpus curvipes | Thysanocarpus curvipes |
| Thysanocarpus curvipes ssp. longistylus | Thysanocarpus curvipes ssp. longistylus |
| Thysanocarpus laciniatus | Thysanocarpus laciniatus |
| Thysanocarpus radians | Thysanocarpus radians |
| Tonella tenella | Tonella tenella |
| Torilis arvensis | Torilis arvensis |
| Torilis nodosa | Torilis nodosa |
| Torreya californica | Torreya californica |
| Toxicodendron diversilobum | Toxicodendron diversilobum |
| Toxicoscordion fremontii | Toxicoscordion fremontii |
| Tragopogon porrifolius | Tragopogon porrifolius |
| Tribulus terrestris | Tribulus terrestris |
| Trichostema lanceolatum | Trichostema lanceolatum |
| Trichostema ruygtii | Trichostema ruygtii |
| Trifolium albopurpureum | Trifolium albopurpureum |
| Trifolium amoenum | Trifolium amoenum |
| Trifolium angustifolium | Trifolium angustifolium |
| Trifolium barbigerum | Trifolium barbigerum |
| Trifolium bifidum | Trifolium bifidum |
| Trifolium bifidum var. bifidum | Trifolium bifidum var. bifidum |
| Trifolium bifidum var. decipiens | Trifolium bifidum var. decipiens |
| Trifolium campestre | Trifolium campestre |
| Trifolium ciliolatum | Trifolium ciliolatum |
| Trifolium columbinum | Trifolium columbinum |
| Trifolium cyathiferum | Trifolium cyathiferum |
| Trifolium depauperatum | Trifolium depauperatum |
| Trifolium depauperatum var. amplectens | Trifolium depauperatum var. amplectens |
| Trifolium depauperatum var. depauperatum | Trifolium depauperatum var. depauperatum |
| Trifolium depauperatum var. truncatum | Trifolium depauperatum var. truncatum |
| Trifolium dubium | Trifolium dubium |
| Trifolium fragiferum | Trifolium fragiferum |
| Trifolium fucatum | Trifolium fucatum |
| Trifolium glomeratum | Trifolium glomeratum |
| Trifolium gracilentum | Trifolium gracilentum |
| Trifolium grayi | Trifolium grayi |
| Trifolium hirtum | Trifolium hirtum |
| Trifolium hybridum | Trifolium hybridum |
| Trifolium hydrophilum | Trifolium hydrophilum |
| Trifolium incarnatum | Trifolium incarnatum |
| Trifolium microcephalum | Trifolium microcephalum |
| Trifolium microdon | Trifolium microdon |
| Trifolium obtusiflorum | Trifolium obtusiflorum |
| Trifolium oliganthum | Trifolium oliganthum |
| Trifolium pratense | Trifolium pratense |
| Trifolium repens | Trifolium repens |
| Trifolium subterraneum | Trifolium subterraneum |
| Trifolium tomentosum | Trifolium tomentosum |
| Trifolium variegatum | Trifolium variegatum |
| Trifolium variegatum var. major | Trifolium variegatum var. major |
| Trifolium variegatum var. variegatum | Trifolium variegatum var. variegatum |
| Trifolium vesiculosum | Trifolium vesiculosum |
| Trifolium willdenovii | Trifolium willdenovii |
| Trifolium wormskioldii | Trifolium wormskioldii |
| Triglochin concinna | Triglochin concinna |
| Triglochin concinna var. concinna | Triglochin concinna var. concinna |
| Triglochin maritima | Triglochin maritima |
| Triglochin scilloides | Triglochin scilloides |
| Triglochin striata | Triglochin striata |
| Triodanis biflora | Triodanis biflora |
| Triphysaria eriantha | Triphysaria eriantha |
| Triphysaria eriantha ssp. eriantha | Triphysaria eriantha ssp. eriantha |
| Triphysaria eriantha ssp. rosea | Triphysaria eriantha ssp. rosea |
| Triphysaria pusilla | Triphysaria pusilla |
| Triphysaria versicolor | Triphysaria versicolor |
| Triphysaria versicolor ssp. faucibarbata | Triphysaria versicolor ssp. faucibarbata |
| Trisetum canescens | Trisetum canescens |
| Triteleia hyacinthina | Triteleia hyacinthina |
| Triteleia laxa | Triteleia laxa |
| Triteleia lugens | Triteleia lugens |
| Triteleia peduncularis | Triteleia peduncularis |
| Triticum aestivum | Triticum aestivum |
| Tropaeolum majus | Tropaeolum majus |
| Tropidocarpum gracile | Tropidocarpum gracile |
| Tuctoria mucronata | Tuctoria mucronata |
| Turritis glabra | Turritis glabra |
| Typha angustifolia | Typha angustifolia |
| Typha domingensis | Typha domingensis |
| Typha latifolia | Typha latifolia |
| Ulmus minor | Ulmus minor |
| Umbellularia californica | Umbellularia californica |
| Uropappus lindleyi | Uropappus lindleyi |
| Urospermum picroides | Urospermum picroides |
| Urtica dioica | Urtica dioica |
| Urtica dioica ssp. holosericea | Urtica dioica ssp. holosericea |
| Urtica urens | Urtica urens |
| Vallisneria australis | Vallisneria australis |
| Verbascum blattaria | Verbascum blattaria |
| Verbascum thapsus | Verbascum thapsus |
| Verbena bonariensis | Verbena bonariensis |
| Verbena hastata | Verbena hastata |
| Verbena lasiostachys | Verbena lasiostachys |
| Verbena lasiostachys var. scabrida | Verbena lasiostachys var. scabrida |
| Verbena litoralis | Verbena litoralis |
| Veronica americana | Veronica americana |
| Veronica anagallis-aquatica | Veronica anagallis-aquatica |
| Veronica arvensis | Veronica arvensis |
| Veronica peregrina | Veronica peregrina |
| Veronica peregrina ssp. xalapensis | Veronica peregrina ssp. xalapensis |
| Veronica persica | Veronica persica |
| Viburnum ellipticum | Viburnum ellipticum |
| Vicia americana | Vicia americana |
| Vicia americana ssp. americana | Vicia americana ssp. americana |
| Vicia benghalensis | Vicia benghalensis |
| Vicia cracca | Vicia cracca |
| Vicia sativa | Vicia sativa |
| Vicia sativa ssp. nigra | Vicia sativa ssp. nigra |
| Vicia sativa ssp. sativa | Vicia sativa ssp. sativa |
| Vicia tetrasperma | Vicia tetrasperma |
| Vicia villosa | Vicia villosa |
| Vicia villosa ssp. varia | Vicia villosa ssp. varia |
| Vicia villosa ssp. villosa | Vicia villosa ssp. villosa |
| Vinca major | Vinca major |
| Vinca minor | Vinca minor |
| Viola douglasii | Viola douglasii |
| Viola pedunculata | Viola pedunculata |
| Viola purpurea | Viola purpurea |
| Viola purpurea ssp. quercetorum | Viola purpurea ssp. quercetorum |
| Vitis californica | Vitis californica |
| Vitis vinifera | Vitis vinifera |
| Washingtonia robusta | Washingtonia robusta |
| Whipplea modesta | Whipplea modesta |
| Woodwardia fimbriata | Woodwardia fimbriata |
| Wyethia angustifolia | Wyethia angustifolia |
| Wyethia glabra | Wyethia glabra |
| Wyethia helenioides | Wyethia helenioides |
| Xanthium spinosum | Xanthium spinosum |
| Xanthium strumarium | Xanthium strumarium |
| Yabea microcarpa | Yabea microcarpa |
| Zannichellia palustris | Zannichellia palustris |
| Zantedeschia aethiopica | Zantedeschia aethiopica |
| Zelkova serrata | Zelkova serrata |
| Zeltnera muehlenbergii | Zeltnera muehlenbergii |
| Zeltnera trichantha | Zeltnera trichantha |

**wi_treatment_file_stage**

| Coded Value | Alias |
|---|---|
| Initial Observation | Initial Observation |
| Approval | Approval |
| Initial Treatment | Initial Treatment |
| Follow Up Treatment | Follow Up Treatment |
| Post Verification Revisit | Post Verification Revisit |

**wi_treatment_stage**

| Coded Value | Alias |
|---|---|
| Initial Observation | Initial Observation |
| Seeking Approval | Seeking Approval |
| Initial Treatment | Initial Treatment |
| Follow Up Treatment | Follow Up Treatment |
| Post Verification Revisit | Post Verification Revisit |
| Complete | Complete |

**wi_yes_no**

| Coded Value | Alias |
|---|---|
| yes | Yes |
| no | No |

**yes no**

| Coded Value | Alias |
|---|---|
| Yes | Yes |
| No | No |
<!-- /GENERATED:domains -->

## 6. Subtypes

<!-- GENERATED:subtypes -->
_No subtypes._
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
| Layer/Table | Relationship | Cardinality |
|---|---|---|
| wi_treatmentpoints | Weeds_X_Invasives_Treatment_Application_wi_r_files | esriRelCardinalityOneToMany |
| wi_treatmentpoints | Weeds_X_Invasives_Treatment_Application_wi_r_treatment_areas | esriRelCardinalityOneToMany |
| wi_r_treatment_areas | Weeds_X_Invasives_Treatment_Application_wi_r_treatment_areas | esriRelCardinalityOneToMany |
| wi_r_files | Weeds_X_Invasives_Treatment_Application_wi_r_files | esriRelCardinalityOneToMany |
<!-- /GENERATED:relationships -->

## 8. Database View Definitions

None. Edit/change-tracking views are documented as a future option, not implemented. The Technical Documentation notes that views could be created to look for changes in the `treatment_stage` attribute and incorporated into the web application, but this was not part of the initial project scope.

## 9. Attribute Rules

None documented.

## 10. Geoprocessing / Automation

None. The Survey123 form and its Inbox-based workflow drive the entire treatment lifecycle process; there are no geoprocessing services or automated scripts associated with this solution.

## 11. Map / App Layer Definitions

### WI Treatment Tracking Points — "Ready to Treat" default

When a new WI Treatment Tracking point is created via the Edit widget in the web application, the **"Ready to Treat"** attribute is automatically defaulted to **No**. This is intentional: with "No" as the default, newly created tracking points remain visible on the map regardless of symbology. If a point were created with "Ready to Treat = Yes" (or left null), it could be filtered out and disappear from the map view immediately upon creation, causing confusion for users.

### Treatment Stage Progression

The `treatment_stage` field on the WI Treatment Tracking points (and throughout the Survey123 form) follows a six-stage lifecycle. Each treatment record progresses through stages in order, edited via the Survey123 Inbox:

| Stage | Description |
|-------|-------------|
| Initial Observation | First contact with the site; species identified and location recorded. |
| Seeking Approval | Waiting for assessee (property owner) and/or tenant approval to treat. |
| Initial Treatment | First treatment applied; result and observer recorded. |
| Follow Up Treatment | Subsequent treatment(s) applied after initial; date and result recorded. |
| Post Verification Revisit | Site revisited to verify treatment effectiveness. |
| Complete | Treatment lifecycle concluded; no further action required. |

One Survey123 record exists per treatment and is updated through its full lifecycle using the Inbox feature. Users must not launch the Survey123 form directly to update an existing treatment — doing so creates a duplicate record. All stage updates are made by retrieving the existing record from the Inbox, editing the appropriate page, and resubmitting.

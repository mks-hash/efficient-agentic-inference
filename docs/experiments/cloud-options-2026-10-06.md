# Cloud hardware choices — price observations, not results

Observed 2026-10-06. Region: Google Cloud `us-central1`, USD list prices.
No GPU run or GPU time/cost measurement has been made. Monetary experiment cost
remains unknown; the values below are planning rates, not measured task costs.

| VM | GPU | On-demand VM USD/hour | Spot VM USD/hour |
| --- | --- | ---: | ---: |
| n2-standard-8 | None; 8 vCPU / 32 GiB RAM | 0.388472 | Not reviewed |
| n1-standard-4 + T4 | 1 T4, 16 GB VRAM | 0.539999 | Not reviewed |
| g2-standard-4 | 1 L4, 24 GB VRAM | 0.706832276 | 0.402848 |
| a2-highgpu-1g | 1 A100, 40 GB VRAM | 3.673385 | 2.20401 |
| a3-highgpu-1g | 1 H100, 80 GB VRAM | Unsupported provisioning model | 6.289417315 |

Rates exclude separately billed disks, IP/network, tax, account currency and
account-specific discounts. The T4 figure adds N1 VM and standalone GPU rates.
G2/A2/A3 figures are full listed VM rates, not bare-card rates. Spot prices are
variable and capacity is interruptible. Quota is not a capacity reservation.
Single/2/4-GPU A3 High instances require Spot or Flex-start. Flex-start rates were
not reviewed here; do not substitute Spot prices for them.

Sources:
- [General-purpose VM pricing](https://cloud.google.com/products/compute/pricing/general-purpose)
- [Standalone GPU pricing](https://cloud.google.com/products/compute/gpus-pricing)
- [Accelerator VM pricing](https://cloud.google.com/products/compute/pricing/accelerator-optimized)
- [Spot pricing](https://cloud.google.com/spot-vms/pricing)
- [Accelerator configuration restrictions](https://docs.cloud.google.com/compute/docs/accelerator-optimized-machines)

## Choose by whole-session economics

For equal useful outcomes, compare rate times total billable duration: provisioning
and software setup, downloads/build, load/warmup, attempted inference and teardown.
For different quality, compare cost per successful localization under the same
contract. Larger GPU memory or peak FLOPS alone cannot determine either result.

At these on-demand rates, A100 must reduce total billable time by more than
5.197 times relative to L4 to become cheaper before other charges. A hypothetical
three-hour L4 session costs USD 2.1205; A100 must finish within about 34.6 minutes
for equal compute cost. One hour of A100 is more expensive than three or four
hours of L4. These are arithmetic scenarios, not runtime predictions.

The proposed three-hour L4 limit is a cap, not an estimated requirement. First
measure a short fixed dev-v1 resource pilot and then estimate the 60-task campaign.
Choose/freeze hardware before generating dev-v2 outputs. Save both setup and
request phases, resource identities, failed attempts and actual billing evidence.
A CUDA run requires its own binary/configuration and physical-isolation checks;
CPU output identity and CPU timing do not imply GPU output identity or economics.

Paid provisioning and execution require explicit run authorization and budget.
No particular provider/hardware is claimed optimal by this planning comparison.
